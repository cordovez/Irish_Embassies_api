from collections import namedtuple
import re
import json
from enum import StrEnum, auto
from models.source import Source

DiplomatName = namedtuple("Name", "first last")


def process_diplomats(data_source: Source) -> list[str]:
    """
    Source.EMBASSIES
    Source.OTHERS
    """
    file_name = data_source.value

    with open(f"data/{file_name}.json", "r") as file:
        json_raw = file.read()
        missions = json.loads(json_raw)

    diplomats = []

    def _process_name(name_str: str):
        if not name_str:
            return DiplomatName("", "")

        match = re.match(r"(\S+)\s+(.+)", name_str)
        first, last = match.groups() if match else (name_str, "")
        return DiplomatName(first, last)

    def _process_mission(mission):
        person = mission["head_of_mission"]
        title = (
            "Ambassador"
            if mission["type_of"] in ["embassy", "other"]
            else "Consul General"
        )

        diplomat = {
            "first_name": _process_name(person).first,
            "last_name": _process_name(person).last,
            "title": title,
            "mission": mission["name"],
        }
        diplomats.append(diplomat)

    for mission in missions:
        if mission["head_of_mission"]:
            _process_mission(mission)

        consulates = mission.get("consulates", [])
        for consulate in consulates:
            if consulate["head_of_mission"]:
                _process_mission(consulate)

    return diplomats


if __name__ == "__main__":
    missions = process_diplomats(Source.EMBASSIES)
    cities = {
        mission["mission"]
        for mission in missions
        if mission["title"] == "Consul General"
    }
    cities_list = sorted(list(cities))

    ambassadors = {
        mission["last_name"].upper()
        + ", "
        + mission["first_name"]
        + f' ({mission["mission"]})'
        for mission in missions
        if mission["title"] == "Ambassador"
    }
    ambassadors_list = sorted(list(ambassadors))
    consuls = {
        mission["last_name"].upper()
        + ", "
        + mission["first_name"]
        + f' ({mission["mission"]})'
        for mission in missions
        if mission["title"] == "Consul General"
    }
    consuls_list = sorted(list(consuls))

    print(ambassadors_list)
