import beanie
from typing import Optional
from mongodb.contact import ContactDetails
from beanie import UnionDoc

from mongodb.diplomat import DiplomatDocument


class MissionUnion(UnionDoc):
    class Settings:
        name = "missions_union"
        class_id: "_class_id"  # noqa: F821


class Mission(beanie.Document):
    head_of_mission: Optional[DiplomatDocument] | None = None
    contact: Optional[ContactDetails] | None = None
    website: Optional[str] | None = None
