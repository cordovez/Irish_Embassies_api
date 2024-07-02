import pydantic
from schemas.contact import ContactDetails
from schemas.diplomat import DiplomatModel
from schemas.consulate import ConsulateModel
# from models.mission import MissionModel
from typing import Optional, Literal


class EmbassyModel(pydantic.BaseModel):
    type_of: Literal["embassy"]
    country: str
    head_of_mission: DiplomatModel | None = None
    contact: Optional[ContactDetails] | None = None
    consulates: Optional[ConsulateModel] | None = (
        None  # I cannot specify type of list object here (i.e. 'Mission') without
        # incurring a circular import
    )

