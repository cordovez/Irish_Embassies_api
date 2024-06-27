import beanie
from fastapi import HTTPException
from mongodb.models import (
    ConsulateDocument,
    EmbassyDocument,
    DiplomatDocument,
    RepresentationDocument,
)
from schemas.enums import MissionType


async def batch_save_to_collection(
    doc: beanie.Document, documents: list[beanie.Document]
) -> dict:
    """
    This Function is intended to be used only to initialise the collection documents created from a json file.
    """
    try:
        if await doc.count() > 0:
            return {"message": "Collection is not empty, no documents were added."}

        result = await doc.insert_many(documents)
        return {"message": f"{len(result.inserted_ids)} documents added successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


async def embassy_append_consulates():
    # consulates = await ConsulateDocument.find().to_list()
    # embassies = await EmbassyDocument.find().to_list()

    for consulate in await ConsulateDocument.find().to_list():
        consulate_host_country = consulate.contact.country

        for embassy in await EmbassyDocument.find().to_list():
            if embassy.host_country.lower() == consulate_host_country.lower():
                consulate_list = embassy.consulates
                consulate_list.append(consulate)

                return await embassy.set({EmbassyDocument.consulates: consulate_list})


# async def match_diplomat_to_mission():
#     """
#     A one-time use function to add head of mission (Diplomat) to an Embassy
#     """
#     for diplomat in await DiplomatDocument.find().to_list():

#         match diplomat.mission_type:
#             case MissionType.EMBASSY:
#                 embassy = await EmbassyDocument.find_one(
#                     EmbassyDocument.host_country == diplomat.mission
#                 )
#                 return await embassy.set({EmbassyDocument.head_of_mission: diplomat})

#             case MissionType.CONSULATE:
#                 consulate = await ConsulateDocument.find_one(
#                     ConsulateDocument.host_city == diplomat.mission
#                 )
#                 return await consulate.set(
#                     {ConsulateDocument.head_of_mission: diplomat}
#                 )


#             case MissionType.REPRESENTATION:
#                 rep = RepresentationDocument.find_one(
#                     RepresentationDocument.representation_name == diplomat.mission
#                 )
#                 return await rep.set({RepresentationDocument.head_of_mission: diplomat})
async def match_diplomat_to_mission() -> list[dict]:
    """
    A one-time use function to add head of mission (Diplomat) to an Embassy
    """
    results = []
    diplomats = await DiplomatDocument.find().to_list()

    for diplomat in diplomats:
        match diplomat.mission_type:
            case MissionType.EMBASSY:
                embassy = await EmbassyDocument.find_one(
                    EmbassyDocument.host_country == diplomat.mission
                )
                if embassy:
                    await embassy.set({EmbassyDocument.head_of_mission: diplomat})
                    results.append(
                        {
                            "mission_type": diplomat.mission_type,
                            "mission": diplomat.mission,
                        }
                    )

            case MissionType.CONSULATE:
                consulate = await ConsulateDocument.find_one(
                    ConsulateDocument.host_city == diplomat.mission
                )
                if consulate:
                    await consulate.set({ConsulateDocument.head_of_mission: diplomat})
                    results.append(
                        {
                            "diplomat": diplomat,
                            "mission_type": diplomat.mission_type,
                            "mission": diplomat.mission,
                        }
                    )

            case MissionType.REPRESENTATION:
                rep = await RepresentationDocument.find_one(
                    RepresentationDocument.representation_name == diplomat.mission
                )
                if rep:
                    await rep.set({RepresentationDocument.head_of_mission: diplomat})
                    results.append(
                        {
                            "mission_type": diplomat.mission_type,
                            "mission": diplomat.mission,
                        }
                    )

    return results
