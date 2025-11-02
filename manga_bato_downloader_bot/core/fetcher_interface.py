from abc import ABC, abstractmethod

class Fetcher(ABC):
    @abstractmethod
    async def fetch_html(self):
        pass
    
    @abstractmethod
    def fetch_title(self) -> str:
        pass

    @abstractmethod
    def fetch_imgs(self) -> list[str]:
        pass
    
    @abstractmethod
    def fetch_current_chapter_name(self) -> str:
        pass

    @abstractmethod
    def fetch_next_chapter_url(self) -> str | None:
        pass
