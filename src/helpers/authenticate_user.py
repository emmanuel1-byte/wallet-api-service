from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer
from typing import Annotated
from fastapi import Depends, HTTPException
from .token import verify_token
from src import User
from beanie import PydanticObjectId


security = HTTPBearer()


async def authenticate_user(
    token: Annotated[HTTPAuthorizationCredentials, Depends(security)]
):
    payload = verify_token(token.credentials)
    user_id = PydanticObjectId(payload.get("sub"))

    user = await User.find_one(User.id == user_id)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail={"message": "Account associated with this token does not exist"},
        )

    return user


AuthDependency = Annotated[HTTPAuthorizationCredentials, Depends(authenticate_user)]
