import pydantic


class DiplomatModel(pydantic.BaseModel):
    last_name: str
    first_name: str
    title: str
    mission: str
