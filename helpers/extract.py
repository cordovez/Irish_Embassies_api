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
            first = process.names_from(item["head_of_mission"]).first
            last = process.names_from(item["head_of_mission"]).last
            mission = item["name"]
            mission_type = process.mission_type_from(item["type_of"])

            diplomats.append(
                DiplomatDocument(
                    first_name=first,
                    last_name=last,
                    mission=process.compound_city_names(mission),
                    mission_type=mission_type,
                )
            )

    return diplomats


def embassies_from_json():
    """
    Function parses JSON file to find embassy (EmbassyDBDoc) data
    """
    embassies = []
    for item in processed_json_data:
        if (
            item["type_of"] == "embassy" and item["head_of_mission"]
        ):  # some items are duplicated in the json file, with empty 'head_of_mission'
            country = item["name"]
            address = item["address"]
            website = item["website"]
            tel = item["tel"]

            contact = ContactDetails(
                address1=address,
                tel=tel,
                city=process.location_from_url(website).city,
                country=country,
            )

            # embassies.append(contact)
            embassies.append(
                EmbassyDocument(
                    contact=contact,
                    website=website,
                    host_country=country,
                )
            )

    return embassies


def consulates_from_json():
    """
    Function parses JSON file to find
    consulate (ConsulateDBDoc) data
    """
    consulates = []
    for item in processed_json_data:
        if (
            item["type_of"] == "consulate" and item["head_of_mission"]
        ):  # some items are duplicated in the json file, with empty 'head_of_mission'
            country = process.location_from_url(item["website"]).country
            address = item["address"]
            website = item["website"]
            tel = item["tel"]

            contact = ContactDetails(
                address1=address,
                tel=tel,
                city=process.location_from_url(website).city,
                country=country,
            )

            # embassies.append(contact)
            consulates.append(
                ConsulateDocument(
                    contact=contact,
                    website=website,
                    host_city=process.location_from_url(website).city,
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
            rep = item["name"]
            website = item["website"]
            address = item["address"]
            tel = item["tel"]

            contact = ContactDetails(
                address1=address,
                tel=tel,
                city=process.location_from_address(item["address"]).city,
                country=process.location_from_address(item["address"]).country,
            )

            # representations.append(contact)
            representations.append(
                RepresentationDocument(
                    contact=contact,
                    website=website,
                    representation_name=rep,
                    host_city=process.location_from_address(item["address"]).city,
                    host_country=process.location_from_address(item["address"]).country,
                )
            )

    return representations


def countries_from_JSON():
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
                    # hosts_type_of_mission= ,
                )
            )
    return countries
