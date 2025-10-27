import os
import httpx
from typing import List, Optional
from manga_bato_downloader_bot.core.fetcher_interface import Fetcher
from manga_bato_downloader_bot.core.playwright_fetcher import PlaywrightFetcher
from .bato_scraper_interface import BatoScraper
from .compressor import Compressor

MANGAS_FOLDER_NAME = 'mangas'

class HttpV3BatoScraper(BatoScraper):
    def __init__(self, link: str):
        self.link = link
        self._archives = []
        self._has_more_chapters = True
        self._title: Optional[str] = None
        self._chapter: Optional[str] = None
        self._compressor = Compressor()
        self._fetcher: Fetcher = PlaywrightFetcher()

    @property
    def has_more_chapters(self) -> bool:
        return self._has_more_chapters

    async def download_next_chapter(self):
        if not self.has_more_chapters:
            return
        
        await self._fetcher.fetch_html(self.link)

        title = await self.get_title()

        self._create_folder(title)

        img_urls = await self._fetcher.fetch_imgs()
        async with httpx.AsyncClient() as client:
            for img_url in img_urls:
                r = await client.get(img_url)
                if r.status_code == 200:
                    filename = f'{img_urls.index(img_url)}.png'
                    module_root = os.path.dirname(os.path.abspath(__file__))
                    manga_path = os.path.join(module_root, MANGAS_FOLDER_NAME, title)

                    with open(os.path.join(manga_path, filename), "wb") as f:
                        f.write(r.content)

        # TODO: Check if folder is bigger than 50 MB

        self._archives.append(self._compressor.compress_folder(title, f'{title}_{len(self._archives)+1}'))

        self._has_more_chapters = False

    async def get_title(self) -> str:
        if self._title is not None:
            return self._title
        
        self._title = await self._fetcher.fetch_title()
        return self._title

    async def get_current_chapter_name(self) -> str:
        self._chapter = await self._fetcher.fetch_current_chapter_name()
        return self._chapter

    def get_manga_zip(self) -> List[str]:
        return self._archives
    
    async def cleanup(self):
        await self._fetcher.stop()

    def _create_folder(self, folder_name: str):
        module_root = os.path.dirname(os.path.abspath(__file__))
        
        manga_path = os.path.join(module_root, MANGAS_FOLDER_NAME)
        os.makedirs(manga_path, exist_ok=True)

        folder_path = os.path.join(manga_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)
