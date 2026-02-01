from abc import ABC, abstractmethod
from .chapter_image import ChapterImage

class MangaScraper(ABC):
    @property
    @abstractmethod
    def has_more_chapters(self) -> bool:
        pass

    @abstractmethod
    async def download_next_chapter(self) -> list[ChapterImage] | None:
        pass

    @abstractmethod
    def get_title(self) -> str:
        pass

    @abstractmethod
    def get_current_chapter_name(self) -> str:
        pass

    @abstractmethod
    def get_reference_img_size(self) -> tuple[int, int] | None:
        pass

    @abstractmethod
    def cleanup(self):
        pass
