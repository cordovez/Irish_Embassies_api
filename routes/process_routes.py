"""
User registration router
"""

from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
from services import extract
from services.process_data import save_missions_to_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


@router.post("/missions", summary="Triages and saves to collections",
             description="Saves embassies, consulates, and representations "
                                  "in mission_union collection")
async def process_missions():
    return await save_missions_to_db()


@router.post(
    "/countries",
    description="extracts countries from scraped data in json file file in "
                "'/data/all_categories.json'",
    summary="saves countries to 'countries' collection in db",
    )
async def process_countries():
    return await extract.all_countries_from_data()
