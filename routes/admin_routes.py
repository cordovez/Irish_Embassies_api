"""
User registration router
"""

from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer

# from helpers.process_data_file import (
#     extract_diplomats,
#     extract_embassies,
#     extract_representations,
# )
from helpers import extract

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


@router.post(
    "/diplomats",
    description="extracts diplomats from scraped data in json file file in '/data/all_categories.json'",
    summary="saves diplomats to db",
)
async def save_diplomats_to_db():
    return extract.diplomats()


@router.post(
    "/embassies",
    description="extracts embassy missions from scraped data in json file file in '/data/all_categories.json'",
    summary="saves embassies to db",
)
async def save_embassies_to_db():
    return extract.embassies()


@router.post(
    "/consulates",
    description="extracts consulate missions from scraped data in json file file in '/data/all_categories.json'",
    summary="saves consulates to db",
)
async def save_consulates_to_db():
    return extract.consulates()


@router.post(
    "/representations",
    description="extracts representation missions from scraped data in json file file in '/data/all_categories.json'",
    summary="saves representations to db",
)
async def representations():
    return extract.representations()


@router.post(
    "/countries",
    description="extracts countries from scraped data in json file file in '/data/all_categories.json'",
    summary="saves representations to db",
)
async def countries():
    return extract.countries()
