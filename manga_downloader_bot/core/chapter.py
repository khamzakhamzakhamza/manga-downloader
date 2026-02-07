from dataclasses import dataclass
from manga_downloader_bot.core.chapter_image import ChapterImage

@dataclass
class Chapter:
    title: str
    chapter_name: str
    imgs: list[ChapterImage]
