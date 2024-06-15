import pydantic
from models.contact import ContactDetails
from models.diplomat import DiplomatModel

# from models.mission import MissionModel
from typing import Optional, Literal


class EmbassyModel(pydantic.BaseModel):
    type_of: Literal["embassy"]
    country: str
    head_of_mission: DiplomatModel | None = None
    contact: Optional[ContactDetails] | None = None
    consulates: Optional[list] | None = (
        None  # I cannot specify type of list object here (i.e. 'Mission') without incurring a circular import
    )
