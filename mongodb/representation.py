import pymongo
from mongodb.mission import Mission
from mongodb.diplomat import DiplomatDocument
from typing import Optional


class RepresentationDocument(Mission):
    head_of_mission: Optional[DiplomatDocument] | None = None
    representation_name: str
    host_city: str
    host_country: str

    class Settings:
        name = "representations"
        indexes = [
            pymongo.IndexModel(
                keys=[("representation_name", pymongo.ASCENDING)],
                name="representation_ascend",
            ),
        ]
