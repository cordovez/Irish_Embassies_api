import pymongo
from mongodb.mission import Mission
from mongodb.entity_type import EntityType


class EmbassyDocument(Mission):
    type_of: EntityType = EntityType.EMBASSY.value

    class Settings:
        name = "embassies"
        indexes = [
            pymongo.IndexModel(
                keys=[("name", pymongo.ASCENDING)],
                name="embassy_ascending",
            ),
        ]
