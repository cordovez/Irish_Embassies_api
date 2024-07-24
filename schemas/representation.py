import pydantic
from typing import Optional


class RepresentationOut(pydantic.BaseModel):
    rep_name: str
    head_of_mission: Optional[str] | None
    address: Optional[str] | None
