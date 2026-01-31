from abc import ABC, abstractmethod

class MangaScraper(ABC):
    @property
    @abstractmethod
    def has_more_chapters(self) -> bool:
        pass

    @abstractmethod
    async def download_next_chapter(self) -> str:
        pass

    @abstractmethod
    def get_title(self) -> str:
        pass

    @abstractmethod
    def get_current_chapter_name(self) -> str:
        pass

    @abstractmethod
    def cleanup(self):
        pass
