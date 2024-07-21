import fastapi
from fastapi import HTTPException, status
from mongodb.diplomat import DiplomatDocument

router = fastapi.APIRouter()


@router.get("/")
async def all_diplomats():
    return await DiplomatDocument.find().to_list()


@router.get("/{dip_id}")
async def by_id(dip_id: str):
    try:
        return await DiplomatDocument.get(dip_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        ) from e
