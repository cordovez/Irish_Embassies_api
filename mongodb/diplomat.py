import pymongo
from mongodb.entity_type import EntityType

import beanie
import pydantic
import pymongo
from typing import Optional


class Diplomat(beanie.Document):
    first_name: str
    last_name: str
    title: Optional[str]
    mission: Optional[str]

    class Settings:
        name = "diplomats"
        indexes = [
            pymongo.IndexModel(
                keys=[("last_name", pymongo.ASCENDING)], name="last_name_ascend"
            ),
        ]
