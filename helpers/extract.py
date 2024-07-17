import json

from mongodb.consulate import ConsulateDocument
from mongodb.contact import ContactDetails
from mongodb.country import CountryDocument
from mongodb.diplomat import DiplomatDocument
from mongodb.embassy import EmbassyDocument
from mongodb.representation import RepresentationDocument

from helpers import process

processed_json_data = process.json_file_from("all_categories")


def diplomats_from_json():
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
