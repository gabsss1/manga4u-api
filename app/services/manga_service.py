import httpx
from collections import defaultdict
from app.models.chapter_model import ChapterImagesResponse

async def fetch_chapters(manga_id: str):
    all_chapters = []
    limit = 100
    offset = 0

    while True:
        url = f"https://api.mangadex.org/chapter?manga={manga_id}&order[chapter]=asc&limit={limit}&offset={offset}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        if response.status_code != 200:
            return {"error": f"No se pudo obtener los capítulos. Status code: {response.status_code}"}

        data = response.json()
        chapters = data.get("data", [])
        all_chapters.extend(chapters)

        total = data.get("total", 0)
        offset += limit

        if offset >= total:
            break

    # Clasificar por idioma
    grouped = defaultdict(list)
    for chapter in all_chapters:
        lang = chapter.get("attributes", {}).get("translatedLanguage", "unknown")
        grouped[lang].append(chapter)

    return grouped

async def get_chapter_images(chapter_id: str) -> ChapterImagesResponse | dict:
    url = f"https://api.mangadex.org/at-home/server/{chapter_id}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code != 200:
        return {"error": f"Capítulo no encontrado: {chapter_id}"}

    data = response.json()
    base_url = data['baseUrl']
    chapter_hash = data['chapter']['hash']
    page_filenames = data['chapter']['data']

    image_urls = [f"{base_url}/data/{chapter_hash}/{filename}" for filename in page_filenames]

    return {
        "chapter_id": chapter_id,
        "total_pages": len(image_urls),
        "images": image_urls
    }

async def get_available_languages(manga_id: str):
    languages = set()
    limit = 100
    offset = 0

    while True:
        url = f"https://api.mangadex.org/chapter?manga={manga_id}&limit={limit}&offset={offset}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        if response.status_code != 200:
            return {"error": f"No se pudo obtener los capítulos. Status code: {response.status_code}"}

        data = response.json()
        chapters = data.get("data", [])
        for chapter in chapters:
            lang = chapter.get("attributes", {}).get("translatedLanguage")
            if lang:
                languages.add(lang)

        total = data.get("total", 0)
        offset += limit

        if offset >= total:
            break

    return sorted(list(languages))

async def fetch_chapters_by_language(manga_id: str, language: str):
    chapters = []
    limit = 100
    offset = 0

    while True:
        url = f"https://api.mangadex.org/chapter?manga={manga_id}&translatedLanguage[]={language}&order[chapter]=asc&limit={limit}&offset={offset}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        if response.status_code != 200:
            return {"error": f"No se pudo obtener los capítulos para el idioma '{language}'."}

        data = response.json()
        chapters.extend(data.get("data", []))

        total = data.get("total", 0)
        offset += limit

        if offset >= total:
            break

    return {"manga_id": manga_id, "language": language, "total_chapters": len(chapters), "chapters": chapters}
