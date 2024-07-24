import pydantic
from typing import Literal
from mongodb.models import DiplomatDocument
from mongodb.contact import ContactDetails
from typing import Optional


class ConsulateOut(pydantic.BaseModel):
    city: str
    head_of_mission: Optional[str]
