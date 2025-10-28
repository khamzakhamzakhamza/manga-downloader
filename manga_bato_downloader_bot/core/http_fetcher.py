import html
import json
import re
from typing import Optional
from curl_cffi.requests import AsyncSession
from .fetcher_interface import Fetcher

class HttpFetcher(Fetcher):
    def __init__(self):
        self.html: Optional[str] = None
    
    async def fetch_html(self, link: str):
        link = f"{link}?zoom=2"

        async with AsyncSession(impersonate="chrome124") as s:
            r = await s.get(link, timeout=30)
            r.raise_for_status()
            self.html = r.text
        
    async def fetch_imgs(self) -> list[str]:
        if self.html is None:
            return []
        
        img_rg = r'<astro-island[^>]*component-url="/_astro/ImageList[^>]*props="([^"]+)"'
        
        match = re.search(img_rg, self.html)
        if not match:
            return []
        
        props_raw = match.group(1)
        imgs = json.loads(html.unescape(props_raw))['imageFiles'][1]
        return [img[1] for img in json.loads(imgs)]
    
    async def fetch_title(self) -> str:
        title_rg = r"<title>(.*?)\s*-"
        return self._search_text(title_rg)
    
    async def fetch_current_chapter_name(self) -> str:        
        chapter_rg = r"<title>.*-\s*(.*?)\s*-"
        return self._search_text(chapter_rg)
    
    async def fetch_next_chapter_url(self) -> str | None:
        if self.html is None:
            return None
        
        next_ch_rg = r'<a[^>]*href="([^"]+)"[^>]*>(?:(?!</a>).)*?(?:Next|▶).*?</a>'

        match = re.search(next_ch_rg, self.html, re.DOTALL)
        if match:
            return match.group(1)
                
        return None

    async def stop(self):
        return
    
    def _search_text(self, pattern: str) -> str:
        if not self.html:
            return ''
        
        match = re.search(pattern, self.html)
        chapter = html.unescape(match.group(1))
        return self._sanitize_path(chapter.strip())

    def _sanitize_path(self, path):
        forbidden_chars = r'[\/:*?"<>|]'
        sanitized_path = re.sub(forbidden_chars, "_", path)  
        return sanitized_path
