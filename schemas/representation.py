import pydantic
from mongodb.contact import ContactDetails
from mongodb.models import DiplomatDocument
from typing import Optional
from typing import Literal


class RepresentationModel(pydantic.BaseModel):
    type_of: Literal["representation"]
    representation: str
    head_of_mission: Optional[DiplomatDocument] | None
    contact: Optional[ContactDetails] | None
