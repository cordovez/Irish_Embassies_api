import pymongo

import beanie
from typing import Optional
from schemas.enums import Grade, Gender, MissionType


class DiplomatDocument(beanie.Document):
    full_name: str
    first_name: str
    last_name: str
    mission_title: str
    mission_type: str

    class Settings:
        name = "diplomats"

