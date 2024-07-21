from fastapi import HTTPException, status
from mongodb.contact import ContactDetails
from mongodb.models import (EmbassyDocument, RepresentationDocument, DiplomatDocument,
                            ConsulateDocument)
from controllers import into_db
from services import from_string, read_data
from typing import List, Any, Dict

RAW_DATA = read_data.from_file_name("all_categories")


# ------------------------------------------------------------------------------
# Main Functions
# ------------------------------------------------------------------------------


async def save_missions_to_db():
    embassies = await _embassies_from_json(RAW_DATA)
    representations = _representations_from_json(RAW_DATA)
    diplomats = _all_diplomats_from_json(RAW_DATA)
    consulates = await _consulates_from_json(RAW_DATA)

    diplomats_response = await into_db.save_many_to_collection(DiplomatDocument,
                                                               diplomats)
    consulates_response = await into_db.save_many_to_collection(ConsulateDocument,
                                                                consulates)
    embassy_response = await into_db.save_many_to_collection(EmbassyDocument, embassies)
    reps_response = await into_db.save_many_to_collection(RepresentationDocument,
                                                          representations)

    return [embassy_response, reps_response, diplomats_response, consulates_response]


# ------------------------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------------------------


def _all_diplomats_from_json(data: List[Dict[str, Any]]) -> list[DiplomatDocument]:
    return [DiplomatDocument(
        first_name=from_string.split_name(item["head_of_mission"]).first,
        last_name=from_string.split_name(item["head_of_mission"]).last,
        mission=from_string.compound_city_names(item["name"]).title(),
        mission_type=from_string.mission_type_from(item["type_of"])
        ) for item in data if item["type_of"] != "country" and item["head_of_mission"]]


async def _consulates_from_json(data: List[Dict[str, Any]]) -> list[ConsulateDocument]:
    consulates = []
    for item in data:
        if item["type_of"] == "consulate" and item["head_of_mission"]:
            name = _create_diplomat(item["head_of_mission"])
            contact = ContactDetails(
                address1=item["address"],
                tel=item["tel"],
                city=from_string.get_mission_location(item["website"]).city.title(),
                country=from_string.get_mission_location(
                    item["website"]).country.title(),
                )

            consulates.append(
                ConsulateDocument(
                    head_of_mission=await _match_diplomat_from_db(name.first_name,
                                                                  name.last_name),
                    contact=contact,
                    website=item["website"],
                    host_city=from_string.get_mission_location(item["website"]).city,
                    )
                )

    return consulates


async def _embassies_from_json(data: List[Dict[str, Any]]) -> list[EmbassyDocument]:
    embassies = []
    for item in data:
        if item["type_of"] == "embassy" and item["head_of_mission"]:
            name = _create_diplomat(item["head_of_mission"])
            contact = ContactDetails(
                address1=item["address"],
                tel=item["tel"],
                city=from_string.get_mission_location(item["website"]).city.title(),
                country=item["name"],
                )
            embassy = EmbassyDocument(
                contact=contact,
                website=item["website"],
                host_country=item["name"],
                consulates=await _process_consulates_from_list(item["consulates"]),
                head_of_mission=await _match_diplomat_from_db(name.first_name,
                                                              name.last_name),
                )
            embassies.append(embassy)

    return embassies


async def _match_diplomat_from_db(first_name: str, last_name: str) -> (DiplomatDocument
                                                                       | None):
    try:
        return await DiplomatDocument.find_one(
            DiplomatDocument.first_name == first_name,
            DiplomatDocument.last_name == last_name)
    except HTTPException(status_code=status.HTTP_404_NOT_FOUND):
        return None


async def _process_consulates_from_list(embassy_consulates: list[dict]) \
        -> list[ConsulateDocument]:
    """
    Takes dict list of consulates and processes some strings before converting to
    consulate objects.
    """
    consulates = []
    for consulate in embassy_consulates:
        name = _create_diplomat(consulate["head_of_mission"])

        contact = ContactDetails(
            address1=consulate["address"],
            tel=consulate["tel"],
            city=from_string.get_mission_location(consulate["website"]).city.title(),
            country=from_string.get_mission_location(
                consulate["website"]).country.title(),
            )

        # embassies.append(contact)
        consulates.append(
            ConsulateDocument(
                head_of_mission=await _match_diplomat_from_db(name.first_name,
                                                              name.last_name),
                contact=contact,
                website=consulate["website"],
                host_city=from_string.get_mission_location(
                    consulate["website"]).city.title(),
                )
            )

    return consulates


def _create_diplomat(fullname: str) -> DiplomatDocument:
    """Takes a full-name string, splits it and creates a diplomat object"""
    return DiplomatDocument(
        first_name=from_string.split_name(fullname).first,
        last_name=from_string.split_name(fullname).last,
        )


def _representations_from_json(data: List[Dict[str, Any]]) \
        -> list[RepresentationDocument]:

    representations = []
    for item in data:
        if item["type_of"] == "other":
            contact = ContactDetails(
                address1=item["address"],
                tel=item["tel"],
                city=from_string.get_mission_location(item["address"]).city,
                country=from_string.get_mission_location(item["address"]).country,
                )

            # representations.append(contact)
            representations.append(
                RepresentationDocument(
                    contact=contact,
                    website=item["website"],
                    representation_name=item["name"],
                    host_city=from_string.get_mission_location(item["address"]).city,
                    host_country=from_string.get_mission_location(
                        item["address"]).country,
                    head_of_mission=_create_diplomat(item["head_of_mission"]),
                    )
                )

    return representations
