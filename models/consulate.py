import pydantic
from typing import Literal
from models.diplomat import DiplomatModel
from models.contact import ContactDetails
from typing import Optional


class ConsulateModel(pydantic.BaseModel):
    type_of: Literal["consulate"]
    city: str
    head_of_mission: DiplomatModel
    contact: Optional[ContactDetails]
