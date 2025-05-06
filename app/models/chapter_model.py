from pydantic import BaseModel
from typing import Optional, List

class Chapter(BaseModel):
    id: str
    volume: Optional[str] = None
    chapter: Optional[str] = None
    title: Optional[str] = None
    translatedLanguage: Optional[str] = None
    publishAt: Optional[str] = None
    readableAt: Optional[str] = None
    pages: Optional[int] = None

class ChapterImagesResponse(BaseModel):
    chapter_id: str
    total_pages: int
    images: List[str]