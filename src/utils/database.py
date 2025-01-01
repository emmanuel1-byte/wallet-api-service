from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from dotenv import load_dotenv
from src import User, Wallet

load_dotenv()
import os


mongodb_client = AsyncIOMotorClient(os.getenv("DATABASE_URI"))


async def initialize_beanie():
    return await init_beanie(database=mongodb_client.Wallet_Service, document_models=[User, Wallet])
