from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


driver.get('https://www.google.com/')

time.sleep(2)

# Close the browser
driver.quit()

print("Driver test done!")
