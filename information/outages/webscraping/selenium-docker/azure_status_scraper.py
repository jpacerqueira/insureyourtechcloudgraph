# import the required libraries
import pandas as pd
import time

#import and use ChromeDriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# instantiate a Chrome options object
options = webdriver.ChromeOptions()

# set the options to use Chrome in headless mode
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")
options.add_argument("--disable-dev-shm-usage")

# initialize an instance of the chrome driver (browser) in headless mode
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)

# Navigate to the website with status history for Azure
#url = "https://azure.status.microsoft/en-gb/status/history"
# Navigate to the website with status current for Azure
url = "https://azure.status.microsoft/en-gb/status/"
driver.get(url)

# Allow the page to load completely
time.sleep(3)

# output the full-page HTML
print(driver.page_source)


# extract all the product containers
zones = driver.find_elements(By.CLASS_NAME, "table status-table table-bordered table-striped fixed-status-header")

# declare an empty list to collect the extracted data
extracted_products = []

# loop through the product containers
for zone in zones:

    # extract the elements into a dictionary using the CSS selector
    data_zone_product_status = {
        "data-zone-name": zone.find_element(By.CLASS_NAME, "data-zone-name").text,
        "status-table-head": zone.find_element(By.CLASS_NAME, "status-table-head").text,
    }

    # append the extracted data to the extracted_product list
    extracted_products.append(data_zone_product_status)

# print the extracted data
print(extracted_products)
# Convert to a DataFrame (extracted_products[0:nnn] if data was collected)
if extracted_products:
    df = pd.DataFrame(extracted_products[0:])
    df.to_csv('output/azure_status_history_extracted_by_products.csv', index=False)


# release the resources allocated by Selenium and shut down the browser
driver.quit()