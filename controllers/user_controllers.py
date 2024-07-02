from fastapi import HTTPException, status


from models.user_model import UserIn
from mongodb.user import UserBase
from auth.password_hasher import get_password_hash


async def create_user(user: UserIn):
    """This function verifies that neither the username nor email passed in as
    'user' parameters, exist in the database.

    if user doesn't already exist, it takes this information information and
    passes it to the to the add_params() function.

    It creates a new user.
    """

    user_email = await UserBase.find_one({"email": user.email})
    user_username = await UserBase.find_one({"username": user.username})
    if user_email is not None:
        raise HTTPException(
            status.HTTP_409_CONFLICT, detail="user with that email already exists"
        )
    if user_username is not None:
        raise HTTPException(
            status.HTTP_409_CONFLICT, detail="user with that username already exists"
        )

    with_added_information = _add_params(user)

    return await UserBase.create(with_added_information)


def _add_params(user_in: UserIn):
    """This function, takes the information passed in from 'create_user' and
    additionally generates:
    • hashed_password
    • uri to a generic avatar image

    It creates a user_dict excluding the password passed through 'UserIn' and
    register the new user.

    """
    hashed_password = get_password_hash(user_in.password)
    user_dict = user_in.dict(exclude={"password"})

    user_name = user_dict["username"]
    uri = f"https://api.multiavatar.com/{user_name}.png"
    avatar_dict = {"public_id": None, "uri": uri}
    return UserBase(
        email=user_dict["email"],
        username=user_dict["username"],
        password_hash=hashed_password,
        avatar=avatar_dict,
    )


async def get_user(id: str):
    """function takes the MongoDB document _id as a string, to search database.
    It has not yet been implemented. It should be limited to a user with "admin"
    privileges.
    """
    found = await UserBase.get(id)
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return found


async def get_users():
    """function returns all users in the database as a list.
    Note: this function should be limited to a user with "admin" privileges
    """
    return await UserBase.find().to_list()


async def update_user_data(user_update_data, current_user):
    """function updates the current_user with the data passed in the
    user_update_data object.
    """
    update_data = user_update_data.dict(exclude_unset=True)

    await UserBase.find_one(UserBase.id == current_user.id).update(
        {"$set": update_data}
    )
    return await UserBase.get(current_user.id)


async def delete_user_by_id(id: str):
    """function takes the MongoDB document _id as a string, to search database
    for document and delete it.

    Note: this function should be limited to a user with "admin" privileges

    """
    user_found = await UserBase.get(id)

    if user_found is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return await user_found.delete()
