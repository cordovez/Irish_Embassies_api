import beanie
import pymongo
from typing import Literal


class CountryDocument(beanie.Document):
    country_name: str
    accredited_to_ireland: bool
    with_mission_in: Literal["dublin", "london"] | None = None
    hosts_irish_mission: bool | None = None
    iso3_code: str | None = None

    class Settings:
        name = "countries"
