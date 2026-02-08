import re
from typing import Optional
from tenacity import retry, stop_after_attempt, wait_exponential
from manga_downloader_bot.core.chapter import Chapter
from manga_downloader_bot.core.scrapers import MangagoScraper, Scraper

class ScrapingOrchestrator:
    def __init__(self, link: str):
        self.link = link
        self._has_more_chapters = True
        self._title: Optional[str] = None
        self._chapter: Optional[str] = None
        self._fetcher: Scraper = MangagoScraper()

    @property
    def has_more_chapters(self) -> bool:
        return self._has_more_chapters

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=5))
    async def download_next_chapter(self) -> Chapter | None:
        if not self.has_more_chapters:
            return None

        await self._fetcher.fetch_html(self.link)

        chapter = Chapter(
            title=self.__get_title(),
            imgs=self._fetcher.fetch_imgs(),
            chapter_name=self.__get_current_chapter_name()
        )

        next_chapter_url = self._fetcher.fetch_next_chapter_url()
        self.link = next_chapter_url
        if not next_chapter_url:
            self._has_more_chapters = False

        return chapter

    def __get_title(self) -> str:
        if self._title is not None:
            return self._title

        self._title = self._fetcher.fetch_title()
        self._title = re.sub(r'[:\\-\\/|?*"<>\']', '', self._title)
        return self._title

    def __get_current_chapter_name(self) -> str:
        self._chapter = self._fetcher.fetch_current_chapter_name()
        return self._chapter

    def cleanup(self):
        self._fetcher.cleanup()
