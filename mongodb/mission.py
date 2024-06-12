import datetime

import beanie
import pydantic
import pymongo
from typing import Optional


class Mission(beanie.Document):
    name: Optional[str] = None
    head_of_mission: Optional[str] = None
    address: Optional[str] = None
    tel: Optional[str] = None
    url: Optional[str] = None
