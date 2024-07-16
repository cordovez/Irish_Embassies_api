
from fastapi import HTTPException, status
from mongodb.country import CountryDocument
import fastapi
from helpers import extract
router = fastapi.APIRouter()


@router.get("/")
async def all_countries():
    return await CountryDocument.find().to_list()


@router.get("/with-irish-embassies")
async def irish_missions_abroad():
    countries = extract.countries_with_embassies()
    return [country for country in countries if country.hosts_irish_mission]


@router.get("/bilateral")
async def missions():
    countries = extract.countries_with_embassies()
    return countries

@router.get("/{country_id}")
async def by_id(country_id: str):
    try:
        return await CountryDocument.get(country_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
            ) from e
