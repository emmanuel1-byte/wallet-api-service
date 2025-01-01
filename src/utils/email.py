from ..services.email.useplunk import send_email
from dotenv import load_dotenv

load_dotenv()
import os


def send_verification_email(firstname: str, email: str, verificaton_token: str):
    return send_email(
        "user_signup",
        email,
        data={
            "Firstname": {"value": firstname, "persistent": False},
            "Verifcation_url": {
                "value": f"{os.getenv("FRONTEND_VERIFICATION_URL")}/{ verificaton_token}",
                "persistent": False,
            },
        },
    )


def send_reset_password_email(firstname: str, email: str, reset_password_token: str):
    return send_email(
        "reset_password",
        email,
        data={
            "Firstname": {"value": firstname, "persistent": False},
            "Reset_password_url": {
                "value": f"{os.getenv("FRONTEND_RESET_PASSWORD_URL")}/{reset_password_token}",
                "persistent": False,
            },
        },
    )
