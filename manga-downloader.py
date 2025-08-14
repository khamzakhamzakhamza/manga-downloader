import os
import re
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image

chapter_url = input('🤖: Paste link to the first chapter here => ')

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
  time.sleep(1)

def get_next_chapter(driver):
  try:
    return driver.find_element(By.XPATH, "//a[@class='btn btn-sm btn-outline btn-primary']/span[text()='Next Chapter ▶']").find_element(By.XPATH, "..").get_attribute('href')
  except NoSuchElementException as _:
    return None

def save_pictures(driver, path, chapter):
  clean_images(path)
  time.sleep(5)
  images = driver.find_elements(By.CSS_SELECTOR, 'div[name="image-item"] img')

  for i, img in enumerate(images):
    try:
      src = img.get_attribute('src')

      file_name = f'{i}.png'
      file_path = os.path.join(path, file_name)

      response = requests.get(src)

      with open(file_path, 'wb') as f:
        f.write(response.content)
    except Exception as e:
      print(f"🤖: Failed to download image. {chapter} {i} {e}")

def create_pdf(title, chapter):
  path = f'mangas/{title}'
  images = []
  
  imgs = [i for i in os.listdir(path) if i.endswith('.png')]

  for i in range(len(imgs)):
    img_path = os.path.join(path, f'{i}.png')
    images.append(Image.open(img_path))

  if images:
    pdf_path = os.path.join(path, f'{title} {chapter}.pdf')
    images[0].save(pdf_path, save_all=True, append_images=images[1:])
    print(f"🤖: Created PDF at {pdf_path}")
  else:
    print("🤖: No images found to create PDF.")

def save_chapter(driver, url):
  driver.get(url)
  
  set_window_size(driver)
  select_zoom_mode(driver)
  click_view_all(driver)

  title = get_title(driver)
  chapter = get_chapter(driver)

  manga_path = f'mangas/{title}'
  os.makedirs(manga_path, exist_ok=True)

  save_pictures(driver, manga_path, chapter)
  create_pdf(title, chapter)

  print(f"🤖: Saved chapter {chapter} from {title} to {manga_path}")

  next_url = get_next_chapter(driver)
  if next_url is None:
    clean_images(manga_path)
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

def clean_images(path):
  for file in os.listdir(path):
    if file.endswith('.png'):
      os.remove(os.path.join(path, file))

print('🤖: Saving BL manga chapters...')
with build_driver() as driver:
  save_chapter(driver, chapter_url)
print('🤖: Max BL capacity reached! 💥(×_×)💥')
