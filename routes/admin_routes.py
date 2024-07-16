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
#     extract_representations,e
# )
from helpers import extract

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


# ------------------------------------------------------------------------------
# Diplomats
# ------------------------------------------------------------------------------
@router.post(
    "/diplomats",
    description="extracts diplomats from scraped data in json file file in "
                "'/data/all_categories.json'",
    summary="saves diplomats to db",
    )
async def save_diplomats_to_db():
    save_diplomats = extract.diplomats_from_json()
    return await in_db.batch_save_to_collection(DiplomatDocument, save_diplomats)


# ------------------------------------------------------------------------------
# Consulates
# ------------------------------------------------------------------------------
@router.post(
    "/consulates",
    description="extracts consulate missions from scraped data in json file file in "
                "'/data/all_categories.json'",
    summary="saves consulates to db",
    )
async def save_consulates_to_db():
    consulates = extract.consulates_from_JSON()
    return await in_db.batch_save_to_collection(ConsulateDocument, consulates)


# ------------------------------------------------------------------------------
# Embassies
# ------------------------------------------------------------------------------
@router.post(
    "/embassies",
    description="extracts embassy missions from scraped data in json file file in "
                "'/data/all_categories.json'",
    summary="saves embassies to db",
    )
async def save_embassies_to_db():
    embassies = extract.embassies_from_json()
    return await in_db.batch_save_to_collection(EmbassyDocument, embassies)


# ------------------------------------------------------------------------------
# Representations
# ------------------------------------------------------------------------------
@router.post(
    "/representations",
    description="extracts representation missions from scraped data in json file file "
                "in '/data/all_categories.json'",
    summary="saves representations to db",
    )
async def asve_representations_to_db():
    representations = extract.representations_from_json()
    return await in_db.batch_save_to_collection(
        RepresentationDocument, representations
        )


# ------------------------------------------------------------------------------
# Countries
# ------------------------------------------------------------------------------
@router.post(
    "/countries",
    description="extracts countries from scraped data in json file file in "
                "'/data/all_categories.json'",
    summary="saves countries to db",
    )
async def save_countries_to_db():
    countries = extract.countries_with_embassies()
    return await in_db.batch_save_to_collection(CountryDocument, countries)
