from enum import StrEnum, auto


class EntityType(StrEnum):
    COUNTRY = auto()
    REPRESENTATION = auto()
    EMBASSY = auto()
    CONSULATE = auto()
