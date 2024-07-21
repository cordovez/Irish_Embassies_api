import pydantic
from typing import Literal
from mongodb.models import DiplomatDocument
from mongodb.contact import ContactDetails
from typing import Optional


class ConsulateModel(pydantic.BaseModel):
    type_of: Literal["consulate"]
    city: str
    head_of_mission: DiplomatDocument
    contact: Optional[ContactDetails]
