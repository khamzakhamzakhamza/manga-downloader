import os
from typing import List, Optional
from .bato_scraper_interface import BatoScraper
from .compressor import Compressor

MANGAS_FOLDER_NAME = 'mangas'

class HttpV3BatoScraper(BatoScraper):
    def __init__(self, link: str):
        self.link = link
        self._archives = []
        self._has_more_chapters = True
        self._folder_path: Optional[str] = None
        self._title: Optional[str] = None
        self._chapter: Optional[str] = None
        self._compressor = Compressor()

    @property
    def has_more_chapters(self) -> bool:
        return self._has_more_chapters

    async def download_next_chapter(self):
        if not self.has_more_chapters:
            return
        
        print(f"Downloading...")

        title = await self.get_title()

        self._create_folder(title)

        # TODO: Check if folder is bigger than 50 MB

        self._archives.append(self._compress_folder(title, f'{title}_{len(self._archives)+1}'))

        self._has_more_chapters = False

    async def get_title(self) -> str:
        if self._title is not None:
            return self._title
        
        self._title = "Test Manga"
        return self._title

    async def get_current_chapter_name(self) -> str:
        if self._chapter is not None:
            return self._chapter
        
        self._chapter = "Test Chapter"
        return self._chapter

    def get_manga_zip(self) -> List[str]:
        return self._archives
    
    def _compress_folder(self, folder_name: str, archive_name: str) -> str:
        archive = self._compressor.compress_folder(folder_name, archive_name)
        return archive

    def _create_folder(self, folder_name: str) -> str:
        module_root = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(module_root, MANGAS_FOLDER_NAME, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        return folder_path
