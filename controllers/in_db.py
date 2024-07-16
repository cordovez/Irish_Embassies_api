import beanie
from fastapi import HTTPException


async def batch_save_to_collection(
    doc: beanie.Document, documents: list[beanie.Document]
) -> dict:
    """
    This Function is intended to be used only to initialise the collection documents
    created from a json file.
    """
    try:
        if await doc.count() > 0:
            return {"message": "Collection is not empty, no documents were added."}

        result = await doc.insert_many(documents)
        return {"message": f"{len(result.inserted_ids)} documents added successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e




