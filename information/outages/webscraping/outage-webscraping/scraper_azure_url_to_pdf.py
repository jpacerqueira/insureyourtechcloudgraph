from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from fpdf import FPDF
import time

def fetch_expanded_content_and_generate_pdf(url, output_file):
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

        # Find all div elements with "Date:" values
        div_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.row.history-dropdowns")))  # Replace 'some-class' with the actual class name
        date_elements = [div for div in div_elements if "Date:" in div.text]

        # Click the 6th "Date:" value (adjusting to zero-based index)
        if len(date_elements) >= 6:
            date_elements[5].click()  # Select the 6th element
            time.sleep(2)  # Allow the page to reload

        # Find and click the div with the "All" "Date:" value
        for div in div_elements:
            if "Date: All" in div.text:  # Adjust the text condition to match the desired "All" option
                div.click()
                time.sleep(2)
                break

        # Expand all collapsible sections
        while True:
            try:
                expand_buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".fxs-progress-details-toggle")))
                if not expand_buttons:
                    break
                for button in expand_buttons:
                    try:
                        button.click()
                        time.sleep(1.5)  # Give it a moment to load the content
                    except:
                        pass  # Continue even if one button fails to click
            except Exception as e:
                print(f"No more expandable elements: {e}")
                break

        # Extract the expanded content
        expanded_content = driver.find_element(By.TAG_NAME, "body").text

        # Generate PDF
        pdf = FPDF(format="A4")
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Write content to PDF with Latin-1 encoding
        lines = expanded_content.split("\n")
        for line in lines:
            if line.strip():  # Skip empty lines
                try:
                    # Convert line to Latin-1 (replace unsupported characters with '?')
                    latin1_line = line.strip().encode('latin-1', errors='replace').decode('latin-1')
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
fetch_expanded_content_and_generate_pdf(url, output_file)
