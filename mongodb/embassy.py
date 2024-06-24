import pymongo
from mongodb.mission import Mission
from mongodb.consulate import ConsulateDocument
from schemas.enums import Level
from typing import Optional


class EmbassyDocument(Mission):
    host_country: str
    consulates: Optional[list[ConsulateDocument]] = []
    level: Level = Level.THREE

    class Settings:
        name = "embassies"
        indexes = [
            pymongo.IndexModel(
                keys=[("host_country", pymongo.ASCENDING)],
                name="embassy_ascending",
            ),
        ]
