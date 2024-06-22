from collections import namedtuple
import re
import json
from mongodb.test_models import MissionType

MissionLocation = namedtuple("MissionLocation", "city country")
DiplomatName = namedtuple("Name", "first last")


def location_from_address(address_str: str) -> tuple:
    """
    Extrapolates city and country from an address string
    """

    if not address_str:
        return MissionLocation("", "")

    pattern = r",\s*([\w\s\-]+)\s*,\s*([\w\s]+)$"

    if match := re.search(pattern, address_str):
        city_raw, country = match.groups()
        city_match = re.search(r"[^\d]+", city_raw)
        city = city_match.group().strip() if city_match else ""
    else:
        city, country = "", ""

    return MissionLocation(city, country.strip())


# def city_from(address_str: str) -> str:
#     """
#     Extrapolates and returns the city (str) from an address string.
#     """
#     pattern = r".*,\s*([\D\s]+)$"


#     if match := re.search(pattern, address_str):
#         city_raw = match[1].strip()
#         return re.findall(r"[^\d]+", city_raw)[-1].strip()
#     return ""
def location_from_url(url: str) -> MissionLocation:
    if not url.startswith("https://www.ireland.ie/en/"):
        return MissionLocation("", "")

    # Regex pattern to match the country and city from the URL
    pattern = r"https://www\.ireland\.ie/en/([\w-]+)/([\w-]+)/"

    if match := re.search(pattern, url):
        country, city = match.groups()
        if country == "usa":
            country = "united states of america"
        if country == "greatbritain":
            country = "great britain"
        city = compound_city_names(city)
        return MissionLocation(city=city, country=country)

    return MissionLocation("", "")


def json_file_from(filename: str) -> list[dict]:
    """
    reads content of json file with a context manager. Returns a list of dictionary items.
    """
    with open(f"data/{filename}.json", "r") as file:
        json_raw = file.read()
    return json.loads(json_raw)


def mission_type_from(mission: str) -> str:
    """
    A switch statement that returns type of mission enum keys: "EMBASSY", "CONSULATE", "REPRESENTATION"
    """
    match mission:
        case "embassy":
            return MissionType.EMBASSY.value

        case "consulate":
            return MissionType.CONSULATE.value
        case _:
            return MissionType.REPRESENTATION.value


def names_from(name_str: str) -> DiplomatName:
    """
    Process a whole name string to extract the first and last name separately.
    """

    if not name_str:
        return DiplomatName("", "")

    match = re.match(r"(\S+)\s+(.+)", name_str)
    first, last = match.groups() if match else (name_str, "")
    return DiplomatName(first, last)


def compound_city_names(city: str) -> str:
    """Cities with compound names have a space missing and are lower case"""
    match city:
        case "sanfrancisco":
            return "san francisco"
        case "newyork":
            return "new york"
        case "losangeles":
            return "los angeles"
        case "hongkong":
            return "hong kong"
        case _:
            return city
