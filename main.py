from fastapi import FastAPI
from src.modules.authentication.route import auth
from src.modules.wallet.route import wallet
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from src.utils.database import initialize_beanie
from src.utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize_beanie()
    print("Database connection succesfull")
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth)
app.include_router(wallet)


@app.get("/", tags=["Health"])
def read_root():
    logger.info("Yeah everyhwere good")
    return JSONResponse(content={"message": "API is running.."}, status_code=200)
