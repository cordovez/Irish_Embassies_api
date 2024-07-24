import pydantic
from typing import Optional


class ContactOut(pydantic.BaseModel):
    address: Optional[str]
    tel: Optional[str]
    website: Optional[str]
