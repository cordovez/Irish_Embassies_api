import beanie
from mongodb.diplomat import DiplomatDocument


async def add_documents_to_mongo(document_model, documents):
    """
    Deletes all documents in a MongoDB collection and Adds new documents to the collection.

    Args:
        document_model: The MongoDB collection model.
        documents: The list of documents (as dictionaries) to add.

    Returns:
        A dictionary with the status of the operation and the count of added documents.
    """

    await document_model.insert_many(documents)
    return {"status": "success", "count": len(documents)}
