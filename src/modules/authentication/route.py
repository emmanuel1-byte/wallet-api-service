from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from .schema import Signup_Schema, Login_Schema, Email_Schema, Reset_Password_Schema
from fastapi.background import BackgroundTasks
from ...utils.email import send_verification_email, send_reset_password_email
from ...helpers.authenticate_user import AuthDependency
from ...services.payment.paystack import Paystack
from ...helpers.token import (
    create_verification_token,
    verify_token,
    create_access_token,
    create_refresh_token,
    create_reset_password_token,
)
from src import User, Wallet
import bcrypt
from beanie import PydanticObjectId


auth = APIRouter(prefix="/api/auth", tags=["Authentication"])


@auth.post("/signup", responses={409: {}})
async def signup(validated_data: Signup_Schema, background_task: BackgroundTasks):
    existing_user = await User.find_one(User.email == validated_data.email)
    if existing_user:
        raise HTTPException(
            status_code=409, detail={"message": "Account already exist"}
        )

    validated_data.password = bcrypt.hashpw(
        validated_data.password.encode(), bcrypt.gensalt()
    ).decode()

    new_user = await User(**validated_data.model_dump()).create()
    await Wallet(user=new_user).create()
    await Paystack().create_customer(new_user)

    verification_token = create_verification_token(new_user.id)
    background_task.add_task(
        send_verification_email,
        new_user.fullname.split(" ")[0],
        new_user.email,
        verification_token,
    )

    return JSONResponse(
        content={
            "data": {"user": new_user.model_dump(mode="json", exclude=["password"])}
        }
    )


@auth.get("/verify-email")
async def verify_email(token: str):
    jwt_payload = verify_token(token)

    user_id = PydanticObjectId(jwt_payload.get("sub"))
    user = await User.find_one(User.id == user_id).set({"verified": True})

    if user is None:
        raise HTTPException(
            status_code=404, detail={"message": "Account does not exist"}
        )

    return JSONResponse(content={"message": "Account verified"}, status_code=200)


@auth.post("/resend-verification-email")
async def resend_verificatin_email(
    validated_data: Email_Schema, background_task: BackgroundTasks
):
    user = await User.find_one(User.email == validated_data.email)
    if user is None:
        raise HTTPException(
            status_code=404, detail={"message": "Account does not exist"}
        )

    if user.verified:
        raise HTTPException(
            status_code=400, detail={"message": "Account already verified"}
        )

    verification_token = create_verification_token(user.id)
    background_task.add_task(
        send_verification_email,
        user.fullname.split(" ")[0],
        user.email,
        verification_token,
    )

    return JSONResponse(content={"message": "Email sent"}, status_code=200)


@auth.post("/login", responses={404: {}, 401: {}, 400: {}})
async def login(validated_data: Login_Schema):
    user = await User.find_one(User.email == validated_data.email)
    if user is None:
        raise HTTPException(
            status_code=404, detail={"message": "Account does not exist"}
        )

    if not user.verified:
        raise HTTPException(
            status_code=400, detail={"message": "Kindly verify your email"}
        )

    comapre_password = bcrypt.checkpw(
        validated_data.password.encode(), user.password.encode()
    )
    if not comapre_password:
        raise HTTPException(status_code=401, detail={"message": "Invalid credentials"})

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return JSONResponse(
        content={
            "data": user.model_dump(mode="json", exclude=["password"]),
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    )


@auth.post("/reset-password")
async def request_password_reset(
    validated_data: Email_Schema, background_task: BackgroundTasks
):
    user = await User.find_one(User.email == validated_data.email)
    if user is None:
        raise HTTPException(
            status_code=404, detail={"message": "Account does not exist"}
        )

    reset_password_token = create_reset_password_token(user.id)
    background_task.add_task(
        send_reset_password_email,
        user.fullname.split(" ")[0],
        user.email,
        reset_password_token,
    )

    return JSONResponse(content={"message": "Email sent"}, status_code=200)


@auth.patch("/reset-password")
async def reset_password(validated_data: Reset_Password_Schema):
    payload = verify_token(validated_data.token)
    user_id = PydanticObjectId(payload.get("sub"))

    user = await User.find_one(User.id == user_id)
    if user is None:
        raise HTTPException(
            status_code=404, detail={"message": "Account does not exist"}
        )

    hashed_password = bcrypt.hashpw(
        validated_data.password.encode(), bcrypt.gensalt()
    ).decode()

    user.password = hashed_password
    await user.save()

    return JSONResponse(
        content={"message": "Password reset succesfull"}, status_code=200
    )


@auth.get("/refresh_token")
async def refresh_token(authenticated_user: AuthDependency):
    user = await User.find_one(User.id == authenticated_user.id)
    if user is None:
        raise HTTPException(
            status_code=404, detail={"message": "Account does not exist"}
        )

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return JSONResponse(
        content={
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    )
