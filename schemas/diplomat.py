import pydantic
from typing import Optional


class DiplomatIn(pydantic.BaseModel):
    full_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    mission_title: Optional[str] = None
    mission_type: Optional[str] = None


class DiplomatOut(pydantic.BaseModel):
    id: str
    full_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    mission_title: Optional[str] = None
    mission_type: Optional[str] = None
