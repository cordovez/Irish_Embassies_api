import pymongo
from mongodb.entity_type import EntityType

import beanie
import pydantic
import pymongo
from typing import Optional


class CountryDocument(beanie.Document):
    type_of: EntityType = EntityType.COUNTRY.value
    name: str
    is_represented: bool
    covered_by: Optional[str]

    class Settings:
        name = "countries"
        indexes = [
            pymongo.IndexModel(
                keys=[("name", pymongo.ASCENDING)],
                name="country_ascend",
            ),
        ]
