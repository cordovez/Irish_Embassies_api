import json
import beanie

from fastapi import HTTPException
from mongodb.consulate import ConsulateDocument
from mongodb.contact import ContactDetails
from mongodb.country import CountryDocument
from mongodb.diplomat import DiplomatDocument
from mongodb.embassy import EmbassyDocument
from mongodb.representation import RepresentationDocument
from mongodb.mission import MissionUnion
from mongodb.models import PublicEmbassyDocument, PublicRepresentationDocument
from controllers import in_db

from helpers import process

processed_json_data = process.json_file_from("all_categories")


# TODO use this function in a "one_route_to_rule_them_all"
async def _save_all_diplomats_to_db():
    diplomats = _diplomats_from_json()
    return await _batch_save_to_collection(DiplomatDocument, diplomats)


async def _collect_all_missions() -> list[beanie.Document]:
    consulates = consulates_from_json()
    embassies = embassies_from_json()
    representations = representations_from_json()

    await _batch_save_to_collection(EmbassyDocument, embassies)
    await _batch_save_to_collection(ConsulateDocument, consulates)
    await _batch_save_to_collection(RepresentationDocument, representations)

    return await MissionUnion.all().to_list()



async def _assign_diplomats(missions: list[beanie.Document]) -> list[beanie.Document]:
    for mission in missions:
        if mission.type_of == 'embassy':
            mission.head_of_mission = await _get_hom(mission.host_country.lower())
        elif mission.type_of == 'consulate':
            mission.head_of_mission = await _get_hom(mission.host_city.lower())
        elif mission.type_of == 'representation':
            mission.head_of_mission = await _get_hom(mission.representation_name.lower())
    return missions


def _match_consulates_to_embassy(missions: list):
    embassies = [mission for mission in missions if mission.type_of == "embassy"]
    consulates = [mission for mission in missions if mission.type_of == "consulate"]
    representations = [mission for mission in missions if mission.type_of ==
                       "representation"]

    for embassy in embassies:
        embassy.contact.city = process.compound_city_names(embassy.contact.city)
        for consulate in consulates:
            if consulate.contact.country.lower() == embassy.host_country.lower():
                embassy.consulates.append(consulate)

    missions = list(embassies)
    missions.extend(iter(representations))

    return missions


async def _get_hom(search_location: str) -> DiplomatDocument:
    city = process.compound_city_names(search_location).lower()
    diplomats = await DiplomatDocument.all().to_list()
    for diplomat in diplomats:
        assigned_mission = process.compound_city_names(diplomat.mission.lower())
        if assigned_mission == city:
            return diplomat


async def _add_to_db(beanie_doc, mission):
    try:
        if await beanie_doc.count() > 0:
            return {"message": "collection is not empty. Nothing was added"}

        result = await beanie_doc(mission).save()
        return {"message": f"{len(result.inserted_ids)} documents added "
                           f"successfully to 'embassies' collection"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


async def _save_public_missions(missions: list[beanie.Document]):
    embassies = [mission for mission in missions if mission.type_of == 'embassy']
    representations = [mission for mission in missions if mission.type_of == 'representation']

    embassy_message = await _batch_save_to_collection(PublicEmbassyDocument, embassies)
    representation_message = await _batch_save_to_collection(PublicRepresentationDocument,
                                                             representations)

    return [embassy_message, representation_message]


async def save_missions_to_db():
    await _save_all_diplomats_to_db()
    missions = await _collect_all_missions()
    populated_missions = await _assign_diplomats(missions)
    embassies_and_reps = _match_consulates_to_embassy(populated_missions)

    return await _save_public_missions(embassies_and_reps)


def _diplomats_from_json() -> list[DiplomatDocument]:
    """
    Function parses JSON file to find diplomat (PersonDBDoc) data
    """
    diplomats = []
    for item in processed_json_data:
        if (
                item["type_of"] != "country" and item["head_of_mission"]
        ):  # some items are duplicated in the json file, with empty 'head_of_mission'

            diplomats.append(
                DiplomatDocument(
                    first_name=process.names_from(item["head_of_mission"]).first,
                    last_name=process.names_from(item["head_of_mission"]).last,
                    mission=process.compound_city_names(item["name"]),
                    mission_type=process.mission_type_from(item["type_of"],
                                                           )
                    ))

    return diplomats


def embassies_from_json():
    """
    Function parses JSON file to find embassy (EmbassyDBDoc) data
    """
    embassies = []
    for item in processed_json_data:
        if item["type_of"] == "embassy" and item["head_of_mission"]:
            contact = ContactDetails(
                address1=item["address"],
                tel=item["tel"],
                city=process.location_from_url(item["website"]).city,
                country=item["name"],
                )
            embassy = EmbassyDocument(
                contact=contact,
                website=item["website"],
                host_country=item["name"],
                )
            embassies.append(embassy)

    return embassies


def consulates_from_json():
    """
    Function parses JSON file to find consulate (ConsulateDBDoc) data
    """
    consulates = []
    for item in processed_json_data:
        if item["type_of"] == "consulate" and item["head_of_mission"]:
            contact = ContactDetails(
                address1=item["address"],
                tel=item["tel"],
                city=process.location_from_url(item["website"]).city,
                country=process.location_from_url(item["website"]).country,
                )

            # embassies.append(contact)
            consulates.append(
                ConsulateDocument(
                    contact=contact,
                    website=item["website"],
                    host_city=process.location_from_url(item["website"]).city,
                    )
                )

    return consulates


def representations_from_json():
    """
    Function parses JSON file to find embassy (EmbassyDBDoc) data
    """
    representations = []
    for item in processed_json_data:
        if item["type_of"] == "other":
            contact = ContactDetails(
                address1=item["address"],
                tel=item["tel"],
                city=process.location_from_address(item["address"]).city,
                country=process.location_from_address(item["address"]).country,
                )

            # representations.append(contact)
            representations.append(
                RepresentationDocument(
                    contact=contact,
                    website=item["website"],
                    representation_name=item["name"],
                    host_city=process.location_from_address(item["address"]).city,
                    host_country=process.location_from_address(item["address"]).country,
                    )
                )

    return representations


def countries_from_json():
    countries = []
    for item in processed_json_data:
        if item["type_of"] == "country":
            countries.append(
                CountryDocument(
                    country_name=item["name"],
                    accredited_to_ireland=process.country_accredited_to_ie(
                        item["name"]
                        ),
                    with_mission_in=process.location_of_foreign_mission_for(
                        item["name"]
                        ),
                    hosts_irish_mission=item["is_represented"],
                    iso3_code=None,
                    )
                )

    return countries


# def countries_with_embassies() -> list[CountryDocument]:
#     """
#     Countries with embassies
#     """
#     embassies = _select_countries_with_embassies(processed_json_data)
#     countries = []
#     for embassy in embassies:
#         embassy = CountryDocument(
#             country_name=embassy["name"],
#             accredited_to_ireland=process.country_accredited_to_ie(
#                 embassy["name"]
#                 ),
#             with_mission_in=process.location_of_foreign_mission_for(embassy["name"]),
#             hosts_irish_mission=embassy["is_represented"],
#             iso3_code=_assign_country_code_to_embassy(embassy),
#
#             )
#
#         countries.append(embassy)
#     return countries


# ------------------------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------------------------
async def _batch_save_to_collection(
    doc: beanie.Document, documents: list[beanie.Document]
) -> dict:
    """
    This Function is intended to be used only to initialise the collection documents
    created from a json file.
    """
    try:
        if await doc.count() > 0:
            return {"message": f"Collection '"
                               f"{doc.__name__.replace('Document','')}s' is not empty, "
                               f"no documents "
                               f"were added"}

        result = await doc.insert_many(documents)
        return {"message": f"{len(result.inserted_ids)} documents added successfully "
                           f"to {doc.__name__.replace('Document','')}s' collection"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


def _assign_country_code_to_embassy(embassy: dict) -> str:
    with open("./data/country_codes_iso.json", "r") as f:
        countries = json.load(f)

    for country in countries:
        if country["name"] == "Slovakia":
            country["name"] = "Slovak Republic"
        if country["name"] == embassy["name"]:
            return country["alpha-3"]


def _select_countries_with_embassies(json_data):
    embassies = []
    for item in json_data:
        item["name"] = _standardize_country_name(item["name"])
        if item["type_of"] == "country" and item["name"] == item["covered_by"]:
            embassies.append(item)
    return embassies


def _standardize_country_name(country_name):
    match country_name:
        case "Korea, Republic of (South Korea)":
            return "Korea, Republic of"
        case "Czech Republic":
            return "Czechia"
        case "Netherlands":
            return "Netherlands, Kingdom of the"
        case "Tanzania":
            return "Tanzania, United Republic of"
        case "Vietnam":
            return "Viet Nam"
        case "Great Britain":
            return "United Kingdom of Great Britain and Northern Ireland"
        case _:
            return country_name
