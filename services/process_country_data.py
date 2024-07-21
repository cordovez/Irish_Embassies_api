from services import  read_data
from controllers import  into_db
from mongodb.models import CountryDocument
from typing import List, Dict, Any
from services import from_string
import csv

RAW_DATA = read_data.from_file_name("all_categories")

# ------------------------------------------------------------------------------
# Main Functions
# ------------------------------------------------------------------------------


async def save_countries_to_db():
    countries = _countries_from_json(RAW_DATA)
    return await into_db.save_many_to_collection(CountryDocument, countries)


# ------------------------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------------------------


def _countries_from_json(data: List[Dict[str, Any]]) -> list[CountryDocument]:
    return [CountryDocument(
                    country_name=item["name"],
                    accredited_to_ireland=_country_accredited_to_ie(
                        item["name"]
                        ),
                    with_mission_in=_location_of_foreign_mission_for(
                        item["name"]
                        ),
                    hosts_irish_mission=item["is_represented"],
                    iso3_code=None,
                    ) for item in data if item["type_of"] == "country"]


def _country_accredited_to_ie(search_country: str) -> bool:

    lower_case_country = search_country.lower()

    with open("data/missions_accredited_to_ireland.csv", "r") as file:
        return lower_case_country in [
            country[0].lower() for country in csv.reader(file)
        ]


def _location_of_foreign_mission_for(country: str) -> str | None:
    with open("data/foreign_missions_in_dublin.csv", "r") as file:
        dublin_missions = [(mission[0], "dublin") for mission in csv.reader(file)]

    with open("data/foreign_missions_in_london.csv", "r") as file:
        london_missions = [(mission[0], "london") for mission in csv.reader(file)]

    foreign_missions = dublin_missions + london_missions
    country = _get_proper_name(country)

    if country is None:
        return None

    for mission in foreign_missions:
        if country in mission[0]:
            return mission[1]


def _get_proper_name(country: str) -> str:
    match country:
        case "United Kingdom of Great Britain and Northern Ireland":
            return "United Kingdom"
        case "Korea, Republic of":
            return "South Korea"
        case "Netherlands, Kingdom of the":
            return "Netherlands"
        case "Russian Federation":
            return "Russia"
        case "Tanzania, United Republic of":
            return "Tanzania"
        case "Viet Nam":
            return "Vietnam"
        case "Slovak Republic":
            return "Slovakia"
        case "Türkiye":
            return "Turkey"
        case "United States of America":
            return "United States"
        case _:
            return country
