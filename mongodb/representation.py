import pymongo
from mongodb.mission import Mission, MissionUnion


class RepresentationDocument(Mission):
    type_of: str = "representation"
    representation_name: str
    host_city: str
    host_country: str

    class Settings:
        name = "representations"
        union_doc = MissionUnion
        indexes = [
            pymongo.IndexModel(
                keys=[("representation_name", pymongo.ASCENDING)],
                name="representation_ascend",
            ),
        ]
