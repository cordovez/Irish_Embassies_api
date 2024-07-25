import pydantic
from typing import Optional


class CountryOut(pydantic.BaseModel):
    id: str
    country_name: str
    accredited_to_ireland: bool
    with_mission_in:  Optional[str] | None = None
    hosts_irish_mission: bool
    iso3_code: str | None

