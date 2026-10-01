from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from neura_engine.command import speak

driver = None

def start_browser():
    global driver
    if driver is None:
        options = Options()
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=options)

def open_website(url):
    start_browser()
    driver.get(url)
    speak(f"Opening {url}...")

def search_on_website(url, search_box_xpath, query):
    start_browser()
    driver.get(url)
    time.sleep(3)
    box = driver.find_element(By.XPATH, search_box_xpath)
    box.send_keys(query)
    box.send_keys(Keys.RETURN)