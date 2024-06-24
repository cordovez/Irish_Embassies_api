import beanie
from typing import Optional
from mongodb.contact import ContactDetails
from mongodb.diplomat import DiplomatDocument


class Mission(beanie.Document):
    head_of_mission: Optional[DiplomatDocument] | None = None
    contact: Optional[ContactDetails] | None = None
    website: Optional[str] | None = None
