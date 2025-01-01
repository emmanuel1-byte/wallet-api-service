import requests
from dotenv import load_dotenv
import asyncio

load_dotenv()
import os


def send_email(event: str, email: str, data: dict):
    response = requests.post(
        "https://api.useplunk.com/v1/track",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv("USEPLUNK_API_KEY")}",
        },
        json={"event": event, "email": email, "data": data},
    )

    if response.status_code == 200:
        print("Email sent succesfully")
    else:
        print(
            f"Failed to send email. Status code: {response.status_code}, Response: {response.text}"
        )

    response.raise_for_status()

