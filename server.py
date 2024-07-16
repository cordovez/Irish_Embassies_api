import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager

from mongodb.db import init_db

# from routes.user_routes import user_route
from routes import (
    token_route,
    embassy_routes,
    admin_routes,
    diplomat_routes,
    user_routes,
    country_routes,
    representation_routes,
    consulate_routes,
    mission_routes,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

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
def root():
    """Route is point of entry and publicly accessible"""
    return {"message": "Ireland's Diplomatic Missions Abroad"}


app.include_router(token_route.router, tags=["Admin"])
app.include_router(country_routes.router, prefix="/countries", tags=["Countries"])

app.include_router(mission_routes.router, prefix="/missions", tags=["Missions"])
app.include_router(embassy_routes.router, prefix="/embassies", tags=["Embassies"])
app.include_router(consulate_routes.router, prefix="/consulates", tags=["Consulates"])
app.include_router(
    representation_routes.router, prefix="/representations", tags=["Representations"]
    )
app.include_router(diplomat_routes.router, prefix="/diplomats", tags=["Diplomats"])
app.include_router(admin_routes.router, prefix="/process", tags=["Admin"])
app.include_router(user_routes.router, tags=["User"])


# app.include_router(token_route, tags=["token"])




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
                "description": "The listing of all countries and their Irish "
                               "diplomatic representative (if any)",
                },
            {
                "name": "Missions",
                "description": "Embassies, consulates, and representations"
                },
            {
                "name": "Embassies",
                "description": "Ambassadorial missions abroad",
                },
            {"name": "Consulates", "description": "Irish Consulates abroad"},
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
    uvicorn.run(reload=True, app="server:app", port=8001)
