import requests
from fastapi import HTTPException
from src import Wallet
from dotenv import load_dotenv

load_dotenv()
import os


class Paystack:

    def __init__(self):
        self.base_url = "https://api.paystack.co"
        self.paystack_secret_key = os.getenv("PAYSTACK_SECRET_KEY")

    async def create_customer(self, user_data):
        print(self.paystack_secret_key, "Paystack secret key....")
        response = requests.post(
            f"{self.base_url}/customer",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.paystack_secret_key }",
            },
            json={
                "email": user_data.email,
                "firstname": user_data.fullname.split(" ")[0],
                "lastname": user_data.fullname.split(" ")[1],
                "phone": user_data.phone,
            },
        )

        if response.status_code == 200:
            response_data = response.json()
            await self.create_virtual_account(
                response_data.get("data").get("customer_code")
            )
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail={"message": "Customer creation failed"},
            )
        response.raise_for_status()

    async def create_virtual_account(self, customer_code: str):
        response = requests.post(
            f"{self.base_url}/dedicated_account",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.paystack_secret_key }",
            },
            json={"customer": customer_code, "preferred_bank": "wema-bank"},
        )

        if response.status_code == 200:
            response_data = response.json()
            print(response_data, "Virtual account.....")

            await Wallet.find_one(
                Wallet.email == response_data.data.get("customer").get("email")
            ).set(
                {
                    "bank": response_data.data.get("bank").get("name"),
                    "account_name": response_data.data.get("account_name"),
                    "account_number": response_data.data.get("account_number"),
                }
            )
        else:
            print(response.json())
            raise HTTPException(
                status_code=response.status_code,
                detail={"message": "Virtual Account creation failed"},
            )
        response.raise_for_status()

    def transfer(self):
        response = requests.post(
            f"{self.base_url}/transfer",
            json={
                "source": "balance",
                "reason": "",
                "amount": "",
            },
        )

    def create_transfer_recipients(self):
        response = requests.post(f"{self.base_url}")
        if response.status_code == 200:
            self.transfer()
        else:
            pass

        response.raise_for_status()
