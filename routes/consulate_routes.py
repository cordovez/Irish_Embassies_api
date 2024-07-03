import fastapi
from controllers import from_missions



router = fastapi.APIRouter()


@router.get("/")
async def all_consulates():
    return await from_missions.get_consulates()


@router.get("/{consulate_id}")
async def by_id(consulate_id):
    return await from_missions.get_mission_by_id(consulate_id)
