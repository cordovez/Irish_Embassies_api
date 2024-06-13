import fastapi
from mongodb.diplomat import DiplomatDocument

router = fastapi.APIRouter()


@router.get("/")
async def all_diplomats():

    return await DiplomatDocument.find().to_list()
