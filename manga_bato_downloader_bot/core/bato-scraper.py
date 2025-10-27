from abc import ABC, abstractmethod

class BatoScraper(ABC):
    @property
    @abstractmethod
    def has_more_chapters(self) -> bool:
        pass
    
    @abstractmethod
    def download_next_chapter(self):
        pass
    
    @abstractmethod
    def get_title(self) -> str:
        pass
    
    @abstractmethod
    def get_current_chapter_name(self) -> str:
        pass
    
    @abstractmethod
    def get_manga_zip(self) -> bytes:
        pass