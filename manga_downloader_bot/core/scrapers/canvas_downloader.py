import io
import math
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver 

class CanvasDownloader:
    @staticmethod
    def download(driver: WebDriver) -> Image:
        canvas = driver.find_element(By.TAG_NAME, "canvas")
        rect = driver.execute_script("return arguments[0].getBoundingClientRect();", canvas)
        scroll_height = 15

        img_chunks: list[Image.Image] = []

        viewport_height = driver.execute_script("return window.innerHeight;")

        chunks_len = math.ceil(rect["height"] / viewport_height)

        driver.execute_script("arguments[0].scrollIntoView();", canvas)
        for _ in range(chunks_len):
            img_chunks.append(Image.open(io.BytesIO(driver.get_screenshot_as_png())))
            driver.execute_script(f"window.scrollBy(0, {viewport_height - scroll_height});")

        combined = Image.new('RGB', (img_chunks[0].width, sum(chunk.height for chunk in img_chunks)))
        space_left = rect["height"]
        y_offset = 0
        for chunk in img_chunks:
            chunk_height = chunk.height - scroll_height
            
            space_left -= chunk_height
            if space_left < 0:
                chunk = chunk.crop((0, abs(space_left), chunk.width, chunk.height))

            combined.paste(chunk, (0, y_offset))
            y_offset += chunk_height

        l = rect["left"]
        r = l + rect["width"]
        b = rect["height"]
        return combined.crop((l, 0, r, b))
