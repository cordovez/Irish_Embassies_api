from enum import StrEnum, auto, IntEnum
from typing import Optional
import pydantic
import beanie


class Level(IntEnum):
    ONE = auto()
    TWO = auto()
    THREE = auto()


class Gender(StrEnum):
    MALE = auto()
    FEMALE = auto()
    NON_BINARY = auto()
    NOT_GIVEN = auto()


class MissionType(StrEnum):
    EMBASSY = auto()
    CONSULATE = auto()
    REPRESENTATION = auto()


class Grade(StrEnum):
    THIRD = "third secretary"
    FIRST = "first secretary"
    COUNSELLOR = "counsellor"
    ASSIST_SEC = "assistant secretary"
    DEP_SEC_GEN = "deputy secretary general"
    SEC_GEN = "secretary general"


class Person(pydantic.BaseModel):
    first_name: str
    last_name: str
    dob: Optional[str] | None = None
    age: Optional[int] | None = None
    grade: Grade = Grade.THIRD.value
    gender: Optional[Gender] | None = None
    mission: Optional[str] | None = None
    hom: bool


class Diplomat(pydantic.BaseModel):
    first_name: str
    last_name: str
    dob: Optional[str] | None = None
    age: Optional[int] | None = None
    grade: Grade | None = None
    gender: Optional[Gender] | None = None
    mission: Optional[str] | None = None
    mission_type: Optional[MissionType] | None = None
    hom: bool = True


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


class Mission(pydantic.BaseModel):
    head_of_mission: Optional[Person] | None = None
    contact: Optional[ContactDetails] | None = None
    website: Optional[str] | None = None


class Country(pydantic.BaseModel):
    country_name: str
    represented_in_dublin: bool = False
    hosts_irish_mission: bool = False
    hosts_type_of_mission: str | None = None


class Consulate(pydantic.BaseModel):
    host_city: str


class Representation(pydantic.BaseModel):
    head_of_mission: Optional[Person] | None = None
    representation_name: str
    host_city: str
    host_country: str


class Embassy(Mission):
    host_country: str
    consulates: Optional[list[Consulate]] = []
    level: Level = Level.THREE
