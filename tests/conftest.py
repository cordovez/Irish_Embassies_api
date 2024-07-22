import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from mongodb.models import CountryDocument


@pytest.fixture(scope="module")
async def test_db():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client.test_db  # Create a test database
    await init_beanie(database=db, document_models=[CountryDocument])

    yield db
    client.close()


@pytest.fixture(autouse=True)
def setup_test_db(test_db):
    pass
