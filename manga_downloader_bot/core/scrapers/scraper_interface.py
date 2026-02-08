from abc import ABC, abstractmethod
from ..chapter_image import ChapterImage

class Scraper(ABC):
    @abstractmethod
    async def fetch_html(self):
        pass

    @abstractmethod
    def fetch_title(self) -> str:
        pass

    @abstractmethod
    def fetch_imgs(self) -> list[ChapterImage]:
        pass

    @abstractmethod
    def fetch_current_chapter_name(self) -> str:
        pass

    @abstractmethod
    def fetch_next_chapter_url(self) -> str | None:
        pass

    @abstractmethod
    def cleanup(self):
        pass
