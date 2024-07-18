import pymongo
from mongodb.consulate import ConsulateDocument
from mongodb.mission import Mission
from typing import Optional, List
from beanie import Link, Document


class PublicEmbassyDocument(Mission):
    host_country: str
    consulates: Optional[List[Link[ConsulateDocument]]] = []

    class Settings:
        name = "embassies_public"
        indexes = [
            pymongo.IndexModel(
                keys=[("host_country", pymongo.ASCENDING)],
                name="embassy_ascending",
                ),
            ]
