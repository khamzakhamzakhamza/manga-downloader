from abc import ABC, abstractmethod

class BatoScraper(ABC):
    @property
    @abstractmethod
    def has_more_chapters(self) -> bool:
        pass
    
    @abstractmethod
    async def download_next_chapter(self) -> str:
        pass
    
    @abstractmethod
    async def get_title(self) -> str:
        pass
    
    @abstractmethod
    async def get_current_chapter_name(self) -> str:
        pass

    @abstractmethod
    async def cleanup(self):
        pass