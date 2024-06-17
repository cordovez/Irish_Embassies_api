from collections import namedtuple
import re
import json
from pprint import pprint
from models.source import Source
from models.diplomat import DiplomatModel

# from models.embassy import EmbassyModel
from models.contact import ContactDetails
from models.mission import MissionModel
from custom_errors.source_file_err import SourceFileError

DiplomatName = namedtuple("Name", "first last")


def extract_diplomats(data_source: Source) -> list[DiplomatModel]:
    """
    Extract diplomats' information from a data source and process compound city names.

    Args:
        data_source: The source of the data containing diplomatic information.

    Returns:
        A list of DiplomatModel instances with processed diplomat information.
    """
    items = _process_json_file(data_source)

    diplomats = []
    for item in items:
        if item["head_of_mission"]:
            diplomats.append(_process_head_of_mission(item))

        if consulates := item.get("consulates", []):
            for consulate in consulates:
                if consulate["head_of_mission"]:
                    diplomats.append(_process_head_of_mission(consulate))

    return _process_compound_city_names(diplomats)


def extract_embassies(data_source: str) -> list[MissionModel]:
    """
    Extract embassy information from a data source and create MissionModel instances.

    Args:
        data_source: The source of the data containing embassy information.

    Returns:
        A list of MissionModel instances representing embassies.
    """

    items = _process_json_file(data_source)
    embassies = []
    for item in items:
        if item["head_of_mission"]:
            person = _process_head_of_mission(item)
            contact = ContactDetails(
                address=item["address"], tel=item["tel"], website=item["website"]
            )
            embassy = MissionModel(
                mission={
                    "type_of": "embassy",
                    "country": item["name"],
                    "head_of_mission": person,
                    "contact": contact,
                    "consulates": _extract_consulates(item),
                }
            )

            embassies.append(embassy)

    return embassies


def extract_representations(data_source: str) -> list[MissionModel]:
    items = _process_json_file(data_source)
    representations = []
    for item in items:
        if item["head_of_mission"]:
            person = _process_head_of_mission(item)
            contact = ContactDetails(
                address=item["address"], tel=item["tel"], website=item["website"]
            )
            representation = MissionModel(
                mission={
                    "type_of": "representation",
                    "representation": item["name"],
                    "head_of_mission": person,
                    "contact": contact,
                }
            )

            representations.append(representation)

    return representations


# ------------------------------------------------------------------------------
# Private Helper functions
# ------------------------------------------------------------------------------


def _process_head_of_mission(item) -> DiplomatModel:
    # diplomats = []
    whole_name = item["head_of_mission"]
    first_name = _process_name(whole_name).first
    last_name = _process_name(whole_name).last
    title = (
        "Ambassador" if item["type_of"] in ["embassy", "other"] else "Consul General"
    )
    mission = item["type_of"]
    location = item["name"]

    return DiplomatModel(
        last_name=last_name,
        first_name=first_name,
        title=title,
        mission=mission,
        location=location,
    )


def _process_json_file(data_source: str) -> list:
    file_name = data_source.value
    if file_name == "countries":
        raise SourceFileError(
            file_name,
            "The selection 'countries' does not contain data that can populate this model",
        )
    with open(f"data/{file_name}.json", "r") as file:
        json_raw = file.read()
    return json.loads(json_raw)


def _extract_consulates(embassy) -> list[MissionModel]:
    consulates = []

    if consulate := embassy.get("consulates", []):
        for consulate in embassy["consulates"]:
            person = _process_head_of_mission(consulate)

            contact = ContactDetails(
                address=consulate["address"],
                tel=consulate["tel"],
                website=consulate["website"],
            )

            consulate = MissionModel(
                mission={
                    "type_of": "consulate",
                    "city": consulate["name"],
                    "head_of_mission": person,
                    "contact": contact,
                }
            )

            consulates.append(consulate)
    return consulates


def _process_name(name_str: str) -> DiplomatName:
    """Process a name string to extract the first and last name components."""
    if not name_str:
        return DiplomatName("", "")

    match = re.match(r"(\S+)\s+(.+)", name_str)
    first, last = match.groups() if match else (name_str, "")
    return DiplomatName(first, last)


def _process_compound_city_names(diplomats) -> list[DiplomatModel]:
    """Cities with compound names have a space missing and are lower case"""
    for diplomat in diplomats:
        match diplomat.mission:
            case "sanfrancisco":
                diplomat.mission = "san francisco"
            case "newyork":
                diplomat.mission = "new york"
            case "losangeles":
                diplomat.mission = "los angeles"
            case "hongkong":
                diplomat.mission = "hong kong"
    return diplomats


# for item in extract_embassies(Source.EMBASSIES):
#     pprint(item.model_dump_json(), indent=4)
# pprint(extract_embassies(Source.EMBASSIES), indent=4)
# print(extract_diplomats(Source.EMBASSIES))