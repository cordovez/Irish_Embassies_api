import pydantic
from typing import Optional


class DiplomatModel(pydantic.BaseModel):
    last_name: str
    first_name: str
    title: Optional[str] | None = None
    mission: Optional[str] | None = None
    location: Optional[str] | None = None
