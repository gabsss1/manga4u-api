from fastapi import APIRouter
from app.services.manga_service import fetch_chapters, get_chapter_images, get_available_languages, fetch_chapters_by_language

router = APIRouter()

@router.get("/chapters-by-language/{manga_id}")
async def get_chapters_by_language(manga_id: str):
    return await fetch_chapters(manga_id)

@router.get("/chapter-images/{chapter_id}")
async def get_images(chapter_id: str):
    return await get_chapter_images(chapter_id)

@router.get("/languages/{manga_id}")
async def get_languages(manga_id: str):
    return await get_available_languages(manga_id)

@router.get("/chapters/{manga_id}/{language}")
async def get_chapters_by_language_and_id(manga_id: str, language: str):
    return await fetch_chapters_by_language(manga_id, language)
