from .authenticate_user import AuthDependency
from src import Wallet
from beanie import PydanticObjectId
from fastapi import HTTPException


async def check_wallet_status(authenticated_user: AuthDependency):
    wallet = await Wallet.find_one(
        Wallet.user.id == PydanticObjectId(authenticated_user.id)
    )
    if wallet is None:
        raise HTTPException(
            status_code=404, detail={"message": "Wallet does not exist"}
        )

    if wallet.status == "Frozen":
        raise HTTPException(
            status_code=401, detail={"message": "Wallet has been frozen"}
        )
    return True
