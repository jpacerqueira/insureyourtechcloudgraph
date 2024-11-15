from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from fpdf import FPDF
import time

def fetch_and_generate_pdf(url, output_file):
    # Setup Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    try:
        # Open the website
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        # Expand all collapsible sections
        while True:
            try:
                # Locate all expandable elements
                expand_buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.fxs-progress-close .fxs-progress-details-toggle')))
                if not expand_buttons:
                    break
                
                for button in expand_buttons:
                    try:
                        button.click()
                        time.sleep(1.5)  # Give it a moment to load
                    except:
                        pass  # Ignore any buttons that can't be clicked again
            except Exception as e:
                print(f"No more collapsible elements to expand: {e}")
                break
        
        # Extract page content
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        content = soup.get_text()

        # Generate PDF
        pdf = FPDF(format='A4')
        pdf.set_auto_page_break(auto=True, margin=12)
        pdf.add_page()
        pdf.set_font("Arial", size=11)

        # Split content into chunks for PDF
        lines = content.split("\n")
        for line in lines:
            if line.strip():  # Avoid adding empty lines
                # Encode line as UTF-16, then decode to Latin-1
                try:
                    utf8_line = line.strip().encode('utf-16', errors='replace').decode('utf-16')
                    latin1_line = utf8_line.encode('latin-1', errors='replace').decode('latin-1')
                    pdf.cell(0, 10, txt=latin1_line, ln=True)
                except Exception as e:
                    print(f"Encoding error for line: {line.strip()}. Error: {e}")
                    continue

        pdf.output(output_file)
        print(f"PDF saved to {output_file}")

    finally:
        driver.quit()

# URL to scrape
# load url and output file from env
from dotenv import load_dotenv
import os
load_dotenv(".env")


url = os.getenv("URL_SCRAPER")
output_file = os.getenv("OUTPUT_FILE")
fetch_and_generate_pdf(url, output_file)
