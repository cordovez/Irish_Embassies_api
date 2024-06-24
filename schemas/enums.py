from enum import StrEnum, auto, IntEnum


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
