import beanie
import pymongo
from typing import Literal


class CountryDocument(beanie.Document):
    country_name: str
    accredited_to_ireland: bool
    with_mission_in: Literal["dublin", "london"] | None = None
    hosts_irish_mission: bool = False

    class Settings:
        name = "countries"
        indexes = [
            pymongo.IndexModel(
                keys=[("country_name", pymongo.ASCENDING)],
                name="country_name_ascending",
            ),
        ]
