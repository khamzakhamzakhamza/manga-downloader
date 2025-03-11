import os
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from PIL import Image

chapter_url = input('🤖: Paste link to the first chapter here => ')

def build_driver():
  options = webdriver.ChromeOptions()
  options.add_argument("--headless")
  options.add_argument("--start-maximized")
  return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def click_view_all(driver):
  btn_text = 'load all pages'
  driver.find_element("xpath", f"//button[text()='{btn_text}']").click()

def get_title(driver):
  title_element = driver.find_element(By.CSS_SELECTOR, 'h3.text-xl a.link-pri.link-hover')
  return sanitize_path(title_element.text)

def get_chapter(driver):
  chapter_element = driver.find_element(By.CSS_SELECTOR, 'h6.text-lg a.link-primary span')
  return sanitize_path(chapter_element.text)

def make_screenshot(driver, path):
  time.sleep(1)

  total_height = driver.execute_script("return document.body.scrollHeight")

  driver.set_window_size(1920, total_height)

  driver.save_screenshot(path)
  with open(path, 'wb') as file:
    file.write(driver.get_screenshot_as_png())

def get_next_chapter(driver):
  try:
    return driver.find_element(By.XPATH, "//a[@class='btn btn-sm btn-outline btn-primary']/span[text()='Next Chapter ▶']").find_element(By.XPATH, "..").get_attribute('href')
  except NoSuchElementException as _:
    return None

def save_chapter(driver, url):
  driver.get(url)
  
  click_view_all(driver)

  title = get_title(driver)
  chapter = get_chapter(driver)

  manga_path = f'mangas/{title}'

  os.makedirs(manga_path, exist_ok=True)
  save_screenshot(driver, manga_path, chapter)

  print(f"🤖: Saved chapter {chapter} from {title} to {manga_path}")

  next_url = get_next_chapter(driver)
  if next_url is None:
    return
  
  save_chapter(driver, next_url)

def sanitize_path(path):
  forbidden_chars = r'[\/:*?"<>|]'
  sanitized_path = re.sub(forbidden_chars, "_", path)  
  return sanitized_path

def save_screenshot(driver, manga_path, chapter):
  path = f'{manga_path}/{chapter}'
  make_screenshot(driver, f'{path}.png')
  convert_png_to_pdf(f'{path}.png', f'{path}.pdf')
  os.remove(f'{path}.png')

def convert_png_to_pdf(png_path, pdf_path):
  image = Image.open(png_path)
  image = image.convert("RGB")
  image.save(pdf_path, "PDF")

print('🤖: Saving BL manga chapters...')
with build_driver() as driver:
  save_chapter(driver, chapter_url)
print('🤖: Max BL capacity reached! 💥(×_×)💥')
