import fastapi
from fastapi import HTTPException, status
from mongodb.consulate import ConsulateDocument

router = fastapi.APIRouter()


@router.get("/")
async def all_consulates():
    return await ConsulateDocument.find().to_list()


@router.get("/{id}")
async def by_id(id: str):
    try:
        return await ConsulateDocument.get(id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        ) from e
