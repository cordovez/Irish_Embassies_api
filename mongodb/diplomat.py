import pymongo

import beanie
from typing import Optional
from schemas.enums import Grade, Gender, MissionType


class DiplomatDocument(beanie.Document):
    first_name: str
    last_name: str
    dob: Optional[str] | None = None
    age: Optional[int] | None = None
    grade: Grade | None = None
    gender: Optional[Gender] | None = None
    mission: Optional[str] | None = None
    mission_type: Optional[MissionType] | None = None
    hom: bool = True

    class Settings:
        name = "diplomats"
        indexes = [
            pymongo.IndexModel(
                keys=[("last_name", pymongo.ASCENDING)], name="last_name_ascend"
            ),
            pymongo.IndexModel(
                keys=[("mission", pymongo.ASCENDING)],
                name="diplomat_mission_ascend",
            ),
        ]
