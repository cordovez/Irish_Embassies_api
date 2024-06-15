from mongodb.user import User
from mongodb.country import CountryDocument
from mongodb.consulate import ConsulateDocument
from mongodb.embassy import EmbassyDocument
from mongodb.representation import RepresentationDocument
from mongodb.diplomat import DiplomatDocument


all_models = [
    User,
    CountryDocument,
    RepresentationDocument,
    EmbassyDocument,
    ConsulateDocument,
    DiplomatDocument,
]
