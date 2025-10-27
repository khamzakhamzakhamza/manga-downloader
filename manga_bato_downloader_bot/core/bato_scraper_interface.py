from abc import ABC, abstractmethod
from typing import List

class BatoScraper(ABC):
    @property
    @abstractmethod
    def has_more_chapters(self) -> bool:
        pass
    
    @abstractmethod
    async def download_next_chapter(self):
        pass
    
    @abstractmethod
    async def get_title(self) -> str:
        pass
    
    @abstractmethod
    async def get_current_chapter_name(self) -> str:
        pass
    
    @abstractmethod
    def get_manga_zip(self) -> List[str]:
        pass