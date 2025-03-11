import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

chapter_url = 'https://bato.to/title/121443-snow-fairy-official/2207331-ch_1'

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
  return title_element.text

def get_chapter(driver):
  chapter_element = driver.find_element(By.CSS_SELECTOR, 'h6.text-lg a.link-primary span')
  return chapter_element.text

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

  next_url = get_next_chapter(driver)
  if next_url is None:
    return
  
  click_view_all(driver)

  title = get_title(driver)
  chapter = get_chapter(driver)

  managa_path = f'mangas/{title}'
  os.makedirs(managa_path, exist_ok=True)
  make_screenshot(driver, f'{managa_path}/{chapter}.png')

  print(f"Saved chapter {chapter} from {title} to {managa_path}")

  save_chapter(driver, next_url)

with build_driver() as driver:
  save_chapter(driver, chapter_url)
