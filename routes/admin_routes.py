"""
User registration router
"""

from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer

# from helpers.process_data_file import (
#     extract_diplomats,
#     extract_embassies,
#     extract_representations,
# )
from helpers import extract

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


# Create
@router.post(
    "/diplomats",
    description="extracts diplomats from spider scraper json file in '/data/'",
    summary="saves diplomats to db",
)
async def save_diplomats_to_db():
    return extract.diplomats()


@router.post(
    "/embassies",
    description="extracts embassy missions from spider scraper json file in '/data/'",
    summary="saves embassies to db",
)
async def save_embassies_to_db():
    return extract.embassies()
    # return await add_documents_to_mongo(DiplomatDocument, document_list)


@router.post(
    "/representations",
    description="extracts representations from selected file and saves to mongodb",
    summary="missions",
)
async def representations():
    pass
    # return extract_representations("others")
    # return await add_documents_to_mongo(DiplomatDocument, document_list)


# @router.get("/diplomats")
# async def get_diplomats():
#     return extract_diplomats()


# @router.post("/add_thing")
# async def add_something(
#     thing: MyThingIn, current_user: Annotated[UserBase, Depends(get_current_user)]
# ) -> MyThingOut:
#     """
#     Route works for currently logged in user.
#     - Takes a "thing" of type: MyThingIn, and adds it to the current logged-in
#     user things.
#     - Returns the added "thing" of type: MyThingOut
#     """

#     result = await add_something_to_user(thing, current_user)
#     return result


# Read
# @router.get("/")
# async def all_embassies(
#     current_user: Annotated[UserBase, Depends(get_current_user)]
# ) -> list:
#     """Route works for currently logged in user.
#     - This route should be reserved
#     for users with "admin" privileges (not implemented)
#     - Returns a list of users of type: UserOut
#     """
#     users_list = await get_embassies()

#     return users_list


# @router.get("/me")
# async def read_user_me(
#     current_user: Annotated[UserBase, Depends(get_current_user)]
# ) -> UserOut:
#     """Route works for currently logged in user.
#     Returns the current user of type: UserOut
#     """
#     return current_user


# @router.get("/my_things")
# async def get_my_things(
#     current_user: Annotated[UserBase, Depends(get_current_user)]
# ) -> list[MyThingOut]:
#     """Route works for currently logged in user.
#     Returns a list of "things" of type: MyThingOut
#     """
#     user = await UserBase.get(current_user.id, fetch_links=True)
#     return user.things


# # Update
# @router.patch("/update")
# async def update_user(
#     update_data: UserUpdate,
#     current_user: Annotated[UserBase, Depends(get_current_user)],
# ) -> UserOut:
#     """Route works for currently logged in user.
#     - It takes update data as a parameter of type: UserUpdate, and updates current user.
#     - Returns updated user of type UserOut
#     """
#     updated_this = await update_user_data(update_data, current_user)
#     return updated_this


# # Delete
# @router.delete("/me/remove")
# async def delete_user(
#     current_user: Annotated[UserBase, Depends(get_current_user)]
# ) -> Message:
#     """
#     Route deletes currently logged in user.
#     """
#     user_has_been_deleted = await delete_user_by_id(current_user.id)

#     return user_has_been_deleted
