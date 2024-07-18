import pymongo
from mongodb.mission import Mission


class PublicRepresentationDocument(Mission):
    representation_name: str

    class Settings:
        name = "representations_public"
        indexes = [
            pymongo.IndexModel(
                keys=[("representation_name", pymongo.ASCENDING)],
                name="ascending_public_representations",
                ),
            ]
