import pydantic
from schemas.consulate import ConsulateOut
from typing import Optional


class EmbassyOut(pydantic.BaseModel):
    id: str
    country: str
    head_of_mission: str | None
    address: Optional[str] | None
    telephone: Optional[str] | None
    consulates: Optional[list[ConsulateOut]] | None = None


