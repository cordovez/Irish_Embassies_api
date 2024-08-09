import pydantic
from typing import Optional


class ContactDetails(pydantic.BaseModel):
    address: Optional[str] = None
    tel: Optional[str] = None
    website: Optional[str] = None


class ContactOut(pydantic.BaseModel):
    address: Optional[str]
    tel: Optional[str]
    website: Optional[str]
