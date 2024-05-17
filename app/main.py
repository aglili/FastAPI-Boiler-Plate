from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.config.database_config import init_db
from app.config.settings import settings
from app.routers.routes import V1_ROUTES

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.get("/")
def index():
    return RedirectResponse("/docs")


for route in V1_ROUTES:
    app.include_router(route, prefix=settings.API_V1_STR)


@app.on_event("startup")
def on_startup():
    init_db()
