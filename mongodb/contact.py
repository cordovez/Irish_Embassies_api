import pydantic
from typing import Optional


class ContactDetails(pydantic.BaseModel):
    address1: Optional[str] | None = None
    address2: Optional[str] | None = None
    address3: Optional[str] | None = None
    address4: Optional[str] | None = None
    city: Optional[str] | None = None
    postal_code: Optional[str] | None = None
    region: Optional[str] | None = None
    country: Optional[str] | None = None
    tel: Optional[str] | None = None
