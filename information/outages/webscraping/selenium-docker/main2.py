
import pandas as pd
import time

#import and use ChromeDriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def app():

  options = webdriver.ChromeOptions()
  options.add_argument("--headless")
  options.add_argument("--no-sandbox")
  options.add_argument("--disable-gpu")
  options.add_argument("--disable-extensions")
  options.add_argument("--disable-dev-shm-usage")


  driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)

  # Navigate to the website
  url = 'https://azure.status.microsoft/en-gb/status/history' 
  driver.get(url)

  # Allow the page to load completely
  time.sleep(2)

  # Find the table element by XPath or CSS selector
  # Adjust the XPath or selector to the specific table
  tables = driver.find_elements(By.TAG_NAME, 'table')  # Find all tables

  # Iterate over the tables and extract data
  all_tables_data = []
  for index, table in enumerate(tables):
    print(f"Extracting Table {index+1}")

    # Get all rows in the table
    rows = table.find_elements(By.TAG_NAME, 'tr')
    table_data = []
    
    for row in rows:
        # Get all cells (columns) in each row
        cells = row.find_elements(By.TAG_NAME, 'td')
        cells_text = [cell.text for cell in cells]
        
        # Append row data to table_data
        table_data.append(cells_text)
    
    # Store data from this table
    all_tables_data.append(table_data)

  # Optionally, save table data to CSV using Pandas
  # Convert to a DataFrame (only for the first table, modify for all tables)
  if all_tables_data:
    df = pd.DataFrame(all_tables_data[0])
    df.to_csv('output/table_data.csv', index=False)

  # Close the browser
  driver.quit()

  print("Google Chrome browser version : " + str(driver.capabilities) + " - Scraping complete. Data saved to table_data.csv.")

  return

if __name__ == "app":
  app
