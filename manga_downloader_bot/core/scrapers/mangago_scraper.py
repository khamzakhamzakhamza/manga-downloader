import io
from urllib.parse import urljoin
import httpx
from PIL import Image
from .scraper_interface import Scraper
from ..chapter_image import ChapterImage
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

class MangagoScraper(Scraper):
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self._reference_img_width: int | None = None

    async def fetch_html(self, link: str):
        self.driver.get(link)
        return

    def fetch_imgs(self) -> list[ChapterImage]:
        pages_count = self.__get_pages_count()
        imgs: list[ChapterImage] = []

        for n in range(pages_count):
            if n > 0:
                self.driver.get(self.__get_next_page_url())
            imgs.append(self.__get_img(n + 1))

        [self.__update_img_width(img) for img in imgs]

        return imgs

    def fetch_title(self) -> str:
        elem = self.driver.find_element(By.ID, "series")
        return elem.text

    def fetch_current_chapter_name(self) -> str:
        elem = self.driver.find_element(By.CSS_SELECTOR, "a.btn.btn-primary.dropdown-toggle.chapter.btn-inverse.top")
        return elem.text

    def fetch_next_chapter_url(self) -> str | None:
        elem = self.driver.find_element(By.CSS_SELECTOR, "a.next_page")
        next_chapter_url = elem.get_attribute("href")

        return next_chapter_url if next_chapter_url and "recommend-manga" not in next_chapter_url else None

    def __get_img(self, page_num: int) -> ChapterImage:
        #TODO: bug here, should just get any element with page
        img_elems = self.driver.find_elements(By.XPATH, f"//img[@id=\"page{page_num}\"]")
        if img_elems:
            src = img_elems[0].get_attribute("src")
            with httpx.Client(verify=False) as client:
                r = client.get(src)
            im = Image.open(io.BytesIO(r.content)).convert("RGB")
            
            if self._reference_img_width is None:
                self._reference_img_width = im.width

            return ChapterImage(image=im, is_canvas=False)
        return ChapterImage(image=self.__screenshot_canvas(), is_canvas=True)

    def __get_pages_count(self) -> int:
        ul_elem = self.driver.find_element(By.ID, "dropdown-menu-page")
        list_items = ul_elem.find_elements(By.TAG_NAME, "li")
        return len(list_items)

    def __get_next_page_url(self) -> str:
        next_link = self.driver.find_element(By.CSS_SELECTOR, "a.next_page[rel=\"next\"]")
        href = next_link.get_attribute("href")
        return urljoin(self.driver.current_url, href)
    
    def __update_img_width(self, ch_img: ChapterImage):
        img = ch_img.image
        aspect_ratio = img.height / img.width
        new_height = int(self._reference_img_width * aspect_ratio)
        ch_img.image = img.resize((self._reference_img_width, new_height), Image.Resampling.LANCZOS)

    def __screenshot_canvas(self) -> Image:
        canvas = self.driver.find_element(By.TAG_NAME, "canvas")

        self.driver.execute_script("document.body.style.zoom='50%'")
        self.driver.execute_script("arguments[0].scrollIntoView();", canvas)

        rect = self.driver.execute_script(
            "return arguments[0].getBoundingClientRect();",
            canvas
        )

        png = self.driver.get_screenshot_as_png()
        im = Image.open(io.BytesIO(png))

        dpr = self.driver.execute_script("return window.devicePixelRatio;")

        l = rect["left"] * dpr
        r = l + rect["width"] * dpr
        b = rect["height"] * dpr
        im = im.crop((l, 0, r, b))

        self.driver.execute_script("document.body.style.zoom='100%'")
        return im.convert("RGB")

    def cleanup(self):
        self.driver.quit()
