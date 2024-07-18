from mongodb.country import CountryDocument
from mongodb.consulate import ConsulateDocument
from mongodb.embassy import EmbassyDocument
from mongodb.representation import RepresentationDocument
from mongodb.diplomat import DiplomatDocument
from mongodb.mission import MissionUnion
from mongodb.user import UserBase
from mongodb.public_embasy import PublicEmbassyDocument
from mongodb.public_representation import PublicRepresentationDocument


all_models = [
    UserBase,
    CountryDocument,
    RepresentationDocument,
    EmbassyDocument,
    ConsulateDocument,
    DiplomatDocument,
    UserBase,
    MissionUnion,
    PublicEmbassyDocument,
    PublicRepresentationDocument,
]
