import pymongo
from mongodb.mission import Mission
from mongodb.entity_type import EntityType


class Consulate(Mission):
    type_of: EntityType = EntityType.CONSULATE.value

    class Settings:
        name = "consulates"
        indexes = [
            pymongo.IndexModel(
                keys=[("name", pymongo.ASCENDING)], name="consulate_ascend"
            ),
        ]
