from mongodb.country import CountryDocument
from mongodb.consulate import ConsulateDocument
from mongodb.embassy import EmbassyDocument
from mongodb.representation import RepresentationDocument
from mongodb.diplomat import DiplomatDocument
from mongodb.mission import MissionUnion
from mongodb.user import UserBase


all_models = [
    UserBase,
    CountryDocument,
    RepresentationDocument,
    EmbassyDocument,
    ConsulateDocument,
    DiplomatDocument,
    UserBase,
    MissionUnion,
]
