from abc import ABC, abstractmethod

class Fetcher(ABC):
    @abstractmethod
    async def fetch_html(self):
        pass
    
    @abstractmethod
    async def fetch_title(self) -> str:
        pass

    @abstractmethod
    async def fetch_imgs(self) -> list[str]:
        pass
    
    @abstractmethod
    async def fetch_current_chapter_name(self) -> str:
        pass

    @abstractmethod
    async def fetch_next_chapter_url(self) -> str | None:
        pass
    
    @abstractmethod
    async def stop(self):
        pass
