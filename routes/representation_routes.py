import fastapi
from controllers import from_missions
from mongodb.public_representation import PublicRepresentationDocument


router = fastapi.APIRouter()


@router.get("/")
async def all_representations():
    reps = await PublicRepresentationDocument.find(fetch_links=True).to_list()

    representations = []
    for rep in reps:
        hom = rep.head_of_mission
        representations.append({"representation": rep.representation_name, "head_of_mission": hom})

    return reps


@router.get("/{rep_id}")
async def by_id(rep_id: str):
    return await from_missions.get_mission_by_id(rep_id)


