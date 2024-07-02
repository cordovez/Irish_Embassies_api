"""
User registration router
"""

from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
from controllers import in_db
from mongodb.models import (
    RepresentationDocument,
    ConsulateDocument,
    EmbassyDocument,
    DiplomatDocument,
    CountryDocument,
)

# from helpers.process_data_file import (
#     extract_diplomats,
#     extract_embassies,
#     extract_representations,
# )
from helpers import extract

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

# ------------------------------------------------------------------------------
# Diplomats
# ------------------------------------------------------------------------------


@router.post(
    "/diplomats",
    description="extracts diplomats from scraped data in json file file in '/data/all_categories.json'",
    summary="saves diplomats to db",
)
async def save_diplomats_to_db():
    save_diplomats = extract.diplomats()
    return await in_db.batch_save_to_collection(DiplomatDocument, save_diplomats)


@router.post(
    "/diplomats/append-to-mission",
    description="Finds mission of type consulate, embassy, or representation and appends its matching diplomat",
    summary="appends diplomats to mission",
)
async def append_diplomats():
    return await in_db.match_diplomat_to_mission()


# ------------------------------------------------------------------------------
# Embassies
# ------------------------------------------------------------------------------


@router.post(
    "/embassies",
    description="extracts embassy missions from scraped data in json file file in '/data/all_categories.json'",
    summary="saves embassies to db",
)
async def save_embassies_to_db():
    save_embassies = extract.embassies()
    return await in_db.batch_save_to_collection(EmbassyDocument, save_embassies)


@router.post(
    "/embassies/add-consulates",
    description="appends consulates to embassies",
    summary="appends consulates",
)
async def append_consulates():
    return await in_db.embassy_append_consulates()


@router.post(
    "/consulates",
    description="extracts consulate missions from scraped data in json file file in '/data/all_categories.json'",
    summary="saves consulates to db",
)
async def save_consulates_to_db():
    save_consulates = extract.consulates()
    return await in_db.batch_save_to_collection(ConsulateDocument, save_consulates)


@router.post(
    "/representations",
    description="extracts representation missions from scraped data in json file file in '/data/all_categories.json'",
    summary="saves representations to db",
)
async def representations():
    save_representations = extract.representations()
    return await in_db.batch_save_to_collection(
        RepresentationDocument, save_representations
    )


@router.post(
    "/countries",
    description="extracts countries from scraped data in json file file in '/data/all_categories.json'",
    summary="saves representations to db",
)
async def save_countries_to_db():
    save_countries = extract.countries()
    return await in_db.batch_save_to_collection(CountryDocument, save_countries)
