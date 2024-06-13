import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from mongodb.db import init_db

# from routes.user_routes import user_route
from routes.token_route import token_route
from routes import embassy_routes, admin_routes, diplomat_routes
from models.message_models import Message


app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["root"])
def root() -> Message:
    """Route is point of entry and publicly accessible"""
    return {"message": "Ireland's Diplomatic Missions Abroad"}


app.include_router(embassy_routes.router, prefix="/embassy", tags=["Embassies"])
app.include_router(admin_routes.router, prefix="/process", tags=["Admin"])
app.include_router(diplomat_routes.router, prefix="/diplomats", tags=["Diplomats"])
# app.include_router(token_route, tags=["token"])


@app.on_event("startup")
async def connect():
    await init_db()


# ------------------------------------------------------------------------------
# OpenAPI Customization
# ------------------------------------------------------------------------------


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    description = """An API to explore the various Irish Diplomatic Missions abroad and bilateral relations in general
    """

    openapi_schema = get_openapi(
        title="Irish Diplomatic Representation Abroad",
        version="1.0.0",
        description=description,
        routes=app.routes,
        tags=[
            {
                "name": "Countries",
                "description": "The listing of all countries and their Irish diplomatic representative (if any)",
            },
            {
                "name": "Embassies",
                "description": "Ambassadorial missions abroad",
            },
            {
                "name": "Representations",
                "description": "Diplomatic missions abroad other than embassies",
            },
            {
                "name": "Diplomats",
                "description": "Diplomats posted abroad ",
            },
            {
                "name": "Admin",
                "description": "API data management",
            },
        ],
    )

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    uvicorn.run(reload=True, app="server:app")
