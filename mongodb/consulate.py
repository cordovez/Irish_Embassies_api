import pymongo
from mongodb.mission import Mission


class ConsulateDocument(Mission):
    host_city: str

    class Settings:
        name = "consulates"
        indexes = [
            pymongo.IndexModel(
                keys=[("host_city", pymongo.ASCENDING)], name="consulate_city"
            ),
        ]
