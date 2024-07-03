import fastapi
from mongodb.representation import RepresentationDocument
from controllers import  from_missions


router = fastapi.APIRouter()


@router.get("/")
async def all_representations():
    return await from_missions.get_representations()


@router.get("/{rep_id}")
async def by_id(rep_id: str):
    return await from_missions.get_mission_by_id(rep_id)
