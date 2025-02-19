from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.main import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("start server ...")
    await init_db()
    yield
    print("server has been stopped")


version = "v1"

app = FastAPI(
    title="ai_mapping",
    description="A REST API for a web ai mapping service",
    version=version,
)
