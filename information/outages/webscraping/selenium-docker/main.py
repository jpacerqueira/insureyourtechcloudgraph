from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")
options.add_argument("--disable-dev-shm-usage")


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)

val = input("Enter a url:")

wait = WebDriverWait(driver, 10)

driver.get(val)

get_url = driver.current_url

wait.until(EC.url_to_be(val))

if get_url == val:
   header=driver.find_element(By.ID, "toc0")

print(header.text)

