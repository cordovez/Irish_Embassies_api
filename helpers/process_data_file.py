from collections import namedtuple
import re
import json
from models.source import Source
from models.diplomat import DiplomatModel
from custom_errors.source_file_err import SourceFileError

DiplomatName = namedtuple("Name", "first last")


def extract_diplomats(data_source: Source) -> list[DiplomatModel]:
    """
    Extract information about diplomats from a JSON file containing diplomatic mission data.

    Args:
        Source.EMBASSIES or Source.OTHERS.

    Returns:
        A list of Diplomat instances with information about diplomats.
    """

    file_name = data_source.value
    if file_name == "countries":
        raise SourceFileError(
            file_name,
            f"The selection '{file_name}' does not contain people information",
        )
    with open(f"data/{file_name}.json", "r") as file:
        json_raw = file.read()
        missions = json.loads(json_raw)

    diplomats = []

    def _process_name(name_str: str):
        """Process a name string to extract the first and last name components."""
        if not name_str:
            return DiplomatName("", "")

        match = re.match(r"(\S+)\s+(.+)", name_str)
        first, last = match.groups() if match else (name_str, "")
        return DiplomatName(first, last)

    def _process_mission(mission):
        """Creates a list of dictionaries containing diplomats' information"""
        person = mission["head_of_mission"]
        title = (
            "Ambassador"
            if mission["type_of"] in ["embassy", "other"]
            else "Consul General"
        )

        diplomat_data = {
            "first_name": _process_name(person).first,
            "last_name": _process_name(person).last,
            "title": title,
            "mission": mission["name"],
        }
        if diplomat_data not in diplomats:
            diplomats.append(diplomat_data)

    for mission in missions:
        if mission["head_of_mission"]:
            _process_mission(mission)

        consulates = mission.get("consulates", [])
        for consulate in consulates:
            if consulate["head_of_mission"]:
                _process_mission(consulate)

    def _process_compound_cities(diplomats):
        """Cities with compound names have a space missing and are lower case"""
        for diplomat in diplomats:
            match diplomat.mission:
                case "Sanfrancisco":
                    diplomat.mission = "San Francisco"
                case "Newyork":
                    diplomat.mission = "New York"
                case "Losangeles":
                    diplomat.mission = "Los Angeles"
                case "Hongkong":
                    diplomat.mission = "Hong Kong"

    diplomats = [
        DiplomatModel(**diplomat) for diplomat in diplomats
    ]  # redifining the list of diplomats from dictionary to list of Diplomat instances

    return diplomats
