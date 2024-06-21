from mongodb.test_models import Diplomat, Embassy, ContactDetails
from helpers import process


processed_json_data = process.json_file_from("all_categories")


def diplomats():
    diplomats = []
    for item in processed_json_data:
        if item["type_of"] != "country" and item["head_of_mission"]:
            first = process.names_from(item["head_of_mission"]).first
            last = process.names_from(item["head_of_mission"]).last
            mission = item["name"]
            mission_type = process.mission_type_from(item["type_of"])

            diplomats.append(
                Diplomat(
                    first_name=first,
                    last_name=last,
                    mission=mission,
                    mission_type=mission_type,
                )
            )

    return diplomats


def embassies():
    def _city_in_string(address: str, embassy_name: str) -> str:
        """
        Some embassy addresses contain the embassy_name name as the last word, others contain the city as the last word.

        This function returns the city based on this distinction.
        """
        if process.location_from(address).country == embassy_name:
            return process.location_from(address).city
        return process.city_from(address)

    embassies = []
    for item in processed_json_data:
        if item["type_of"] == "embassy" and item["head_of_mission"]:
            country = item["name"]
            address = item["address"]
            website = item["website"]
            tel = item["tel"]

            contact = ContactDetails(
                address1=address,
                tel=tel,
                city=_city_in_string(address, country),
                country=country,
            )

            # embassies.append(contact)
            embassies.append(
                Embassy(
                    contact=contact,
                    website=website,
                    host_country=country,
                )
            )

    return embassies
