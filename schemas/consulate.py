import pydantic
from typing import Optional


class ConsulateOut(pydantic.BaseModel):
    id: Optional[str] | None = None  # id only needed for consulates route
    city: str
    head_of_mission: Optional[str]
