import pydantic
from typing import Optional
from schemas.contact import ContactDetails
from schemas.diplomat import DiplomatIn, DiplomatOut
from mongodb.models import DiplomatDocument


class RepresentationOut(pydantic.BaseModel):
    id: str
    rep_name: str
    head_of_mission: Optional[str]
    address: Optional[str]


class RepresentationIn(pydantic.BaseModel):
    head_of_mission: Optional[DiplomatIn] = None
    contact: Optional[ContactDetails] = None
    website: Optional[str] = None
    representation_name: Optional[str] = None
    host_city: Optional[str] = None
    host_country: Optional[str] = None
