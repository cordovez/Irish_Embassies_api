"""
User registration router
"""

from fastapi import APIRouter, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from auth.current_user import get_current_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


# Create
@router.get("/")
async def embassies():
    pass


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
