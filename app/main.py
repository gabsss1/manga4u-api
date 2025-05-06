from fastapi import FastAPI
from app.routes import manga_routes

app = FastAPI(
    title="Manga4U API",
    description="API para obtener capítulos e imágenes de MangaDex.",
    version="1.0.0"
)

app.include_router(manga_routes.router)