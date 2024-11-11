import time
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# URL of the Yahoo Finance page with the AAPL stock data
url = 'https://finance.yahoo.com/quote/AAPL/history/'

# Initialize driver variable
driver = None

try:
    # Set up Selenium WebDriver with options
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run Chrome in headless mode
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Open the page in Selenium
    driver.get(url)

    # Wait for the page to load (adjust time if needed)
    time.sleep(5)

    # Get the page source after it has loaded JavaScript content
    html = driver.page_source

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Locate the table with the historical data
    table = soup.find('table')

    # Extract all rows in the table
    rows = table.find_all('tr')

    # Prepare the list to hold the extracted data
    table_data = []

    # Extract the header row
    header = [th.text.strip() for th in rows[0].find_all('th')]
    table_data.append(header)

    # Extract data rows
    for row in rows[1:]:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        table_data.append(cols)

    # Write the extracted data to a CSV file
    with open('AAPL_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(table_data)

    print("Data has been written to AAPL_data.csv")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser after the task is completed, if driver is initialized
    if driver:
        driver.quit()
