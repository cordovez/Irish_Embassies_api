import pydantic
from schemas.contact import ContactOut
from schemas.diplomat import DiplomatOut
from schemas.consulate import ConsulateOut
# from models.mission import MissionModel
from typing import Optional
from pydantic import ConfigDict


class EmbassyOut(pydantic.BaseModel):
    country: str
    head_of_mission: str | None
    address: Optional[str] | None
    telephone: Optional[str] | None
    consulates: Optional[list[ConsulateOut]] | None = None


