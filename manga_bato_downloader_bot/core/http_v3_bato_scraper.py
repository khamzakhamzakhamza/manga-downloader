import os
import httpx
from typing import List, Optional
from manga_bato_downloader_bot.core.fetcher_interface import Fetcher
from manga_bato_downloader_bot.core.playwright_fetcher import PlaywrightFetcher
from .bato_scraper_interface import BatoScraper
from .compressor import Compressor
from PIL import Image

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
            for i, img_url in enumerate(img_urls):
                r = await client.get(img_url)
                await self._save_img(f'{i}.png', r.content)
        
        await self._create_pdf()
        await self._clean_images()

        # TODO: Check if folder is bigger than 50 MB

        self._archives.append(self._compressor.compress_folder(title, f'{title}_{len(self._archives)+1}'))

        next_chapter_url = await self._fetcher.fetch_next_chapter_url()
        if next_chapter_url:
            self.link = f'https://bato.to{next_chapter_url}'
        else:
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

    async def _save_img(self, name: str, img: bytes):
        module_root = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(module_root, MANGAS_FOLDER_NAME, await self.get_title(), name)

        with open(img_path, "wb") as f:
            f.write(img)
    
    async def _create_pdf(self):
        module_root = os.path.dirname(os.path.abspath(__file__))
        manga_path = os.path.join(module_root, MANGAS_FOLDER_NAME, await self.get_title())
        images = []
        
        imgs = [i for i in os.listdir(manga_path) if i.endswith('.png')]

        for i in range(len(imgs)):
            img_path = os.path.join(manga_path, f'{i}.png')
            images.append(Image.open(img_path))

        if images:
            pdf_path = os.path.join(manga_path, f'{await self.get_title()} {await self.get_current_chapter_name()}.pdf')
            images[0].save(pdf_path, save_all=True, append_images=images[1:])
    
    async def _clean_images(self):
        module_root = os.path.dirname(os.path.abspath(__file__))
        manga_path = os.path.join(module_root, MANGAS_FOLDER_NAME, await self.get_title())

        for file in os.listdir(manga_path):
            if file.endswith('.png'):
                os.remove(os.path.join(manga_path, file))
