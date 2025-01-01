from fastapi import APIRouter, Body, Header, HTTPException
from typing import Annotated
import bcrypt
from fastapi.responses import JSONResponse
from .model import Wallet
from src import User
from ...helpers.authenticate_user import AuthDependency
from beanie import PydanticObjectId
from .schema import Set_Pin_Schema, Transfer_Schema
from cryptography.hazmat.primitives.hmac import HMAC
from dotenv import load_dotenv
import json
from ...enums.enum import Wallet_status

load_dotenv()

import os

wallet = APIRouter(prefix="/api/users/wallet", tags=["Wallet"])


@wallet.patch("/set-pin")
async def set_wallet_pin(validated_data: Set_Pin_Schema):
    user = await User.find_one(User.email == validated_data.email)
    if user is None:
        raise HTTPException(
            status_code=404, detail={"message": "Account does not exist"}
        )

    wallet = await Wallet.find_one(Wallet.user.id == user.id)

    wallet.pin = bcrypt.hashpw(validated_data.pin.encode(), bcrypt.gensalt()).decode()
    await wallet.save()

    return JSONResponse(
        content={"message": "Your wallet pin has been set"}, status_code=200
    )


@wallet.patch("/freeze")
async def freeze_wallet(authenticated_user: AuthDependency):
    wallet = await Wallet.find_one(
        Wallet.user.id == PydanticObjectId(authenticated_user.id)
    ).set({"status": Wallet_status.FROZEN})

    if wallet is None:
        raise HTTPException(
            status_code=404, detail={"message": "Wallet does not exist"}
        )

    return JSONResponse(content={"message": "Wallet frozen"})


@wallet.patch("/unfreeze")
async def freeze_wallet(authenticated_user: AuthDependency):
    wallet = await Wallet.find_one(
        Wallet.user.id == PydanticObjectId(authenticated_user.id)
    ).set({"status": Wallet_status.UNFROZEN})

    if wallet is None:
        raise HTTPException(
            status_code=404, detail={"message": "Wallet does not exist"}
        )

    return JSONResponse(content={"message": "Wallet frozen"})


@wallet.post("/transfer")
async def transfer_funds(
    validated_data: Transfer_Schema, authenticated_user: AuthDependency
):
    wallet = await Wallet.find_one(
        Wallet.user.id == PydanticObjectId(authenticated_user.id), fetch_links=True
    )

    if wallet is None:
        raise HTTPException(
            status_code=404, detail={"message": "Wallet does not exist"}
        )

    if wallet.balance == 0:
        raise HTTPException(
            status_code=400, detail={"message": "Insufficient funds my brother"}
        )

    # call Paystack transfer endpoint
    return JSONResponse(content={"message": "Transfer successfull"})


@wallet.get("/me")
async def get_my_wallet(authenticated_user: AuthDependency):
    wallet = await Wallet.find_one(
        Wallet.user.id == PydanticObjectId(authenticated_user.id), fetch_links=True
    )

    if wallet is None:
        raise HTTPException(
            status_code=404, detail={"message": "Wallet does not exist"}
        )

    del wallet.user.password
    return JSONResponse(
        content={"data": {"wallet": wallet.model_dump(mode="json")}},
        status_code=200,
    )


@wallet.post("/paystack-webhook")
def paystack_webhook(
    paystack_response: Annotated[dict, Body()],
    x_paystack_signature: Annotated[str, Header()],
):
    hash = HMAC(os.getenv("PAYSTACK_SECRET_KEY"), algorithm="sha512").update(
        json.dumps(paystack_response)
    )
    if hash == x_paystack_signature:
        match (paystack_response.get("event")):
            case "charge.success":
                pass
            case "transfer.success":
                pass
    return JSONResponse(status_code=200)
