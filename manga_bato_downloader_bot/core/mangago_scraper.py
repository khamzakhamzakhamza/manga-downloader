import re
import httpx
from typing import Optional
from tenacity import retry, stop_after_attempt, wait_exponential
from manga_bato_downloader_bot.core.file_manager import FileManager
from manga_bato_downloader_bot.core.selenium_fetcher import SeleniumFetcher
from .fetcher_interface import Fetcher
from .scraper_interface import MangaScraper

MANGAS_FOLDER_NAME = 'mangas'

class MangagoScraper(MangaScraper):
    def __init__(self, link: str):
        self.link = link
        self._has_more_chapters = True
        self._title: Optional[str] = None
        self._chapter: Optional[str] = None
        self._fetcher: Fetcher = SeleniumFetcher()
        self._file_manager = FileManager()

    @property
    def has_more_chapters(self) -> bool:
        return self._has_more_chapters

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=5))
    async def download_next_chapter(self) -> str | None:
        if not self.has_more_chapters:
            return

        await self._fetcher.fetch_html(self.link)

        title = self.get_title()
        self._file_manager.create_folder(title)

        img_urls = self._fetcher.fetch_imgs()
        with httpx.Client(verify=False) as client:
            for i, img_url in enumerate(img_urls):
                try:
                    if isinstance(img_url, str):
                        r = client.get(img_url)
                        self._file_manager.save_img(title, f'{i}.png', r.content)
                    else:
                        self._file_manager.save_img_pil(title, f'{i}.png', img_url)
                except Exception as ex:
                    print(ex)

        chapter_pdf_path = self._file_manager.create_pdf(title, self.get_current_chapter_name())
        self._file_manager.clean_images(title)

        next_chapter_url = self._fetcher.fetch_next_chapter_url()
        self.link = next_chapter_url
        if not next_chapter_url:
            self._has_more_chapters = False

        if chapter_pdf_path:
            return chapter_pdf_path
        return None

    def get_title(self) -> str:
        if self._title is not None:
            return self._title
        
        self._title = self._fetcher.fetch_title()
        self._title = re.sub(r'[:\\-\\/|?*"<>\']', '', self._title)
        return self._title

    def get_current_chapter_name(self) -> str:
        self._chapter = self._fetcher.fetch_current_chapter_name()
        return self._chapter

    def cleanup(self):
        # self._file_manager.clean_folder(self.get_title())
        pass
