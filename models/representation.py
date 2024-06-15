import pydantic
from models.contact import ContactDetails
from models.diplomat import DiplomatModel
from typing import Optional
from typing import Literal


class RepresentationModel(pydantic.BaseModel):
    type_of: Literal["representation"]
    representation: str
    head_of_mission: Optional[DiplomatModel] | None
    contact: Optional[ContactDetails] | None
