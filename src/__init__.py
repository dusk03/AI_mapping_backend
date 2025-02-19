from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.auth.routers import auth_router
from .middleware import register_middleware
from .errors import register_all_errors


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

register_middleware(app)
register_all_errors(app)

app.include_router(auth_router, prefix="/api/{version}/auth", tags=["auth"])
