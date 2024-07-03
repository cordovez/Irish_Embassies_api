import beanie
from typing import Optional
from mongodb.contact import ContactDetails
from beanie import Link, UnionDoc

from mongodb.diplomat import DiplomatDocument


class MissionUnion(UnionDoc):
    class Settings:
        name = "mission_union"
        class_id: "_class_id"


class Mission(beanie.Document):
    head_of_mission: Optional[Link[DiplomatDocument]] | None = None
    contact: Optional[ContactDetails] | None = None
    website: Optional[str] | None = None
