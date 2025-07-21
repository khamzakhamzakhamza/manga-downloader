import os
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image

chapter_url = input('🤖: Paste link to the first chapter here => ')

def load_all_images(driver):
  time.sleep(2)
  images = driver.find_elements(By.TAG_NAME, 'img')
  print(f'🤖: Found {len(images)} images. Waiting for them to load...')

  for i in range(len(images)):
    img = driver.find_elements(By.TAG_NAME, 'img')[i]
    if not img.is_displayed():
      continue

    WebDriverWait(driver, 10).until(lambda d: img.get_attribute('complete'))

def build_driver():
  options = webdriver.ChromeOptions()
  options.add_argument("--headless")
  options.add_argument("--disable-gpu")
  return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def click_view_all(driver):
  select_element = WebDriverWait(driver, 10).until(
      EC.visibility_of_element_located((By.CSS_SELECTOR, "select[data-name='page-load']"))
  )

  select = Select(select_element)
  select.select_by_value("2")

def get_title(driver):
  title_element = driver.find_element(By.CSS_SELECTOR, 'h3.text-xl a.link-pri.link-hover')
  return sanitize_path(title_element.text)

def get_chapter(driver):
  chapter_element = driver.find_element(By.CSS_SELECTOR, 'h6.text-lg a.link-primary span')
  return sanitize_path(chapter_element.text)

def set_window_size(driver):
  window_width = 1100

  driver.set_window_size(window_width, 600)
  driver.execute_script("window.scrollTo(0, 0);")
  time.sleep(5)

def take_screenshot(driver, path, chapter, attempt=0):
  window_width = 1100
  max_height = 58000
  split = False

  height = driver.execute_script("return document.body.scrollHeight") - attempt * max_height
  if height > max_height:
    print(f'🤖: {chapter} is too long! Splitting into multiple screenshots...')
    height = max_height
    split = True

  driver.set_window_size(window_width, height)
  driver.execute_script(f"window.scrollTo(0, {attempt * max_height});")
  time.sleep(1)

  file_name = f'{chapter}{f'-{attempt}'}'
  png_path = f'{path}/{file_name}.png'
  
  driver.save_screenshot(png_path)
  convert_png_to_pdf(png_path, path, file_name)
  os.remove(png_path)

  if split:
    take_screenshot(driver, path, chapter, attempt+1)

def get_next_chapter(driver):
  try:
    return driver.find_element(By.XPATH, "//a[@class='btn btn-sm btn-outline btn-primary']/span[text()='Next Chapter ▶']").find_element(By.XPATH, "..").get_attribute('href')
  except NoSuchElementException as _:
    return None

def save_chapter(driver, url):
  driver.get(url)
  
  set_window_size(driver)
  select_zoom_mode(driver)
  click_view_all(driver)
  load_all_images(driver)

  title = get_title(driver)
  chapter = get_chapter(driver)

  manga_path = f'mangas/{title}'

  os.makedirs(manga_path, exist_ok=True)
  take_screenshot(driver, manga_path, chapter)

  print(f"🤖: Saved chapter {chapter} from {title} to {manga_path}")

  next_url = get_next_chapter(driver)
  if next_url is None:
    return
  
  save_chapter(driver, next_url)

def sanitize_path(path):
  forbidden_chars = r'[\/:*?"<>|]'
  sanitized_path = re.sub(forbidden_chars, "_", path)  
  return sanitized_path

def select_zoom_mode(driver):
  select_element = WebDriverWait(driver, 10).until(
      EC.visibility_of_element_located((By.CSS_SELECTOR, "select[data-name='page-zoom']"))
  )

  select = Select(select_element)
  select.select_by_value("2")

def convert_png_to_pdf(png_path, path, file_name):
  pdf_path = f'{path}/{file_name}.pdf'
  image = Image.open(png_path)
  image = image.convert("RGB")
  image.save(pdf_path, "PDF")

print('🤖: Saving BL manga chapters...')
with build_driver() as driver:
  save_chapter(driver, chapter_url)
print('🤖: Max BL capacity reached! 💥(×_×)💥')
