"""
User registration router
"""

from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
from controllers import in_db, from_missions
from mongodb.models import (
    RepresentationDocument,
    ConsulateDocument,
    EmbassyDocument,
    DiplomatDocument,
    CountryDocument, PublicEmbassyDocument, MissionUnion, PublicRepresentationDocument
    )

from helpers import extract

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

@router.post("/missions")
async def process_missions():
    return await extract.save_missions_to_db()

# ------------------------------------------------------------------------------
# Diplomats
# ------------------------------------------------------------------------------
@router.post(
    "/diplomats",
    description="extracts diplomats from scraped data in json file file in "
                "'/data/all_categories.json'",
    summary="saves diplomats to 'diplomats' collection db",
    )
async def save_diplomats_to_db():
    save_diplomats = extract._diplomats_from_json()
    return await in_db.batch_save_to_collection(DiplomatDocument, save_diplomats)


# ------------------------------------------------------------------------------
# Consulates
# ------------------------------------------------------------------------------
@router.post(
    "/consulates",
    description="extracts consulate missions from scraped data in json file file in "
                "'/data/all_categories.json'",
    summary="saves consulates to 'missions_union' collection db",
    )
async def save_consulates_to_db():
    consulates = extract.consulates_from_json()
    return await in_db.batch_save_to_collection(ConsulateDocument, consulates)


# ------------------------------------------------------------------------------
# Embassies
# ------------------------------------------------------------------------------
@router.post(
    "/embassies",
    description="extracts embassy missions from scraped data in json file file in "
                "'/data/all_categories.json'",
    summary="saves embassies to 'missions_union' collection in db",
    )
async def save_embassies_to_db():
    embassies = extract.embassies_from_json()
    return await in_db.batch_save_to_collection(EmbassyDocument, embassies)


@router.post("/public-embassies")
async def save_populated_embassies_to_db():
    embassies = await from_missions.get_embassies()
    return await in_db.batch_save_to_collection(PublicEmbassyDocument, embassies)


# ------------------------------------------------------------------------------
# Representations
# ------------------------------------------------------------------------------
@router.post(
    "/representations",
    description="extracts representation missions from scraped data in json file file "
                "in '/data/all_categories.json'",
    summary="saves representations to 'missions_union' collection in db",
    )
async def save_representations_to_db():
    representations = extract.representations_from_json()
    return await in_db.batch_save_to_collection(
        RepresentationDocument, representations
        )

#TODO head of missions not being added to document
@router.post("/public-representations")
async def save_populated_representations_to_db():
    representations = await from_missions.get_representations()
    return await in_db.batch_save_to_collection(PublicRepresentationDocument, representations)


# ------------------------------------------------------------------------------
# Countries
# ------------------------------------------------------------------------------
@router.post(
    "/countries",
    description="extracts countries from scraped data in json file file in "
                "'/data/all_categories.json'",
    summary="saves countries to 'countries' collection in db",
    )
async def save_countries_to_db():
    countries = extract.countries_with_embassies()
    return await in_db.batch_save_to_collection(CountryDocument, countries)
