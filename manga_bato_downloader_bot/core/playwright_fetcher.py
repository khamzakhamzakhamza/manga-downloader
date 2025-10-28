import re
from playwright.async_api import async_playwright
from .fetcher_interface import Fetcher

class PlaywrightFetcher(Fetcher):
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None
    
    async def fetch_html(self, link: str):
        if not self.browser:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=False)
        
        self.page = await self.browser.new_page()
        await self.page.goto(link, timeout=60000)
        await self.page.wait_for_load_state("domcontentloaded")
        
        load = await self.page.wait_for_selector("select[data-name='page-load']")
        await load.select_option("2")
        
        zoom = await self.page.wait_for_selector("select[data-name='page-zoom']")
        await zoom.select_option("2")
        
    async def fetch_imgs(self) -> list[str]:
        img_urls = []
        await self.page.wait_for_selector("div[name=\"image-item\"] img")
        imgs = await self.page.query_selector_all('div[name="image-item"] img')
        
        for img in imgs:
            src = await img.get_attribute("src")
            img_urls.append(src)
            
        return img_urls
    
    async def fetch_title(self) -> str:
        title_element = await self.page.wait_for_selector("h3.text-xl a.link-pri.link-hover")
        title_text = await title_element.inner_text() if title_element else None
        return self._sanitize_path(title_text)
    
    async def fetch_current_chapter_name(self) -> str:
        chapter_element = await self.page.wait_for_selector("h6.text-lg a.link-primary span")
        chapter_text = await chapter_element.inner_text() if chapter_element else None
        return self._sanitize_path(chapter_text)
    
    async def fetch_next_chapter_url(self) -> str | None:
        try:
            next_chapter_element = await self.page.wait_for_selector("//a[@class='btn btn-sm btn-outline btn-primary']/span[text()='Next Chapter ▶']", timeout=5000)
            parent = await next_chapter_element.evaluate_handle("node => node.parentElement")
            href = await parent.get_attribute("href")
            return href
        except:
            return None

    async def stop(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    def _sanitize_path(self, path):
        forbidden_chars = r'[\/:*?"<>|]'
        sanitized_path = re.sub(forbidden_chars, "_", path)  
        return sanitized_path
