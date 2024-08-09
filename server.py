import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager

from mongodb.db import init_db

# from routes.user_routes import user_route
from routes import (
    token_route,
    user_routes,
    public_routes,
    private_routes,
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

app.include_router(public_routes.router, prefix="/public", tags=["Public"])

app.include_router(user_routes.router, tags=["User"])

app.include_router(private_routes.router, prefix="/private", tags=["Private"])


# app.include_router(token_route, tags=["token"])


# ------------------------------------------------------------------------------
# OpenAPI Customization
# ------------------------------------------------------------------------------


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    description = """An API to explore the various Irish Diplomatic Missions abroad 
    and bilateral relations in general
    """

    openapi_schema = get_openapi(
        title="Irish Diplomatic Representation Abroad",
        version="1.0.0",
        description=description,
        routes=app.routes,
        tags=[
            {
                "name": "Public",
                "description": "Read-only populated missions. Intended for public "
                               "access",
                },
            {
                "name": "Private",
                "description": "Create and Update missions. Intended for administrator "
                               "only ",
                },

            ],
        )

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

if __name__ == "__main__":
    uvicorn.run(reload=True, app="server:app", port=8001)
