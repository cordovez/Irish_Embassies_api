import pydantic
from typing import Optional


class DiplomatOut(pydantic.BaseModel):
    last_name: str
    first_name: str
    title: Optional[str] | None = None

