import pymongo
from mongodb.mission import Mission
from mongodb.entity_type import EntityType


class Representation(Mission):
    type_of: EntityType = EntityType.REPRESENTATION.value

    class Settings:
        name = "representations"
        indexes = [
            pymongo.IndexModel(
                keys=[("name", pymongo.ASCENDING)], name="representation_ascend"
            ),
        ]
