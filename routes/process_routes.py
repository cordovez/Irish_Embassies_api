"""
User registration router
"""

from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
from services import extract
from services import process_mission_data, process_country_data

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


@router.post("/missions", summary="Triages and saves to collections",
             description="Saves embassies, consulates, and representations "
                                  "in mission_union collection")
async def process_missions():
    return await process_mission_data.save_missions_to_db()


@router.post(
    "/countries",
    description="extracts countries from scraped data in json file file in "
                "'/data/all_categories.json'",
    summary="saves countries to 'countries' collection in db",
    )
async def process_countries():
    return await process_country_data.save_countries_to_db()
