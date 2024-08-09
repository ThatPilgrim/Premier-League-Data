# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup
# import csv

# # Set up Selenium WebDriver
# options = webdriver.ChromeOptions()
# options.add_argument('--ignore-certificate-errors')
# driver = webdriver.Chrome()

# # URL of the webpage (replace with the actual URL)
# url = 'https://www.sofascore.com/tournament/football/england/premier-league/17#id:52186'
# driver.get(url)

# # Increase wait time if necessary
# wait = WebDriverWait(driver, 60)  # Waits up to 30 seconds

# try:
#     # Wait for the table to be present on the page
#     table_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table.sc-dZoequ.fFnwuy')))
    
#     # Parse the page source with BeautifulSoup
#     soup = BeautifulSoup(driver.page_source, 'html.parser')
    
#     # Locate the table
#     table = soup.find('table', class_='sc-dZoequ fFnwuy')
    
#     if table:
#         # Extract and write data to CSV
#         with open(r'C:\Users\manny\Documents\SofaScoreLiveRating\table_data.csv', 'w', newline='', encoding='utf-8') as file:
#             writer = csv.writer(file)
#             headers = [th.get_text(strip=True) for th in table.find('thead').find_all('th')]
#             writer.writerow(headers)
#             for row in table.find('tbody').find_all('tr'):
#                 data = [td.get_text(strip=True) for td in row.find_all('td')]
#                 writer.writerow(data)
#         print("Table data extracted and saved to CSV.")
#     else:
#         print("Table not found.")
# except Exception as e:
#     print(f"An error occurred: {e}")
# finally:
#     # Close the browser
#     driver.quit()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import time

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(options=options)

# URL of the webpage (replace with the actual URL)
url = 'https://www.sofascore.com/tournament/football/england/premier-league/17#id:52186'
driver.get(url)

# Increase wait time if necessary
wait = WebDriverWait(driver, 45)  # Waits up to 45 seconds

# Open the CSV file in append mode
with open(r'C:\Users\manny\Documents\SofaScoreLiveRating\table_data.csv', 'a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    while True:
        try:
            # Wait for the table to be present on the page
            table_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table.sc-dZoequ.fFnwuy')))
            
            # Parse the page source with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # Locate the table
            table = soup.find('table', class_='sc-dZoequ fFnwuy')

            if table:
                if file.tell() == 0:  # Check if the file is empty to write headers
                    headers = [th.get_text(strip=True) for th in table.find('thead').find_all('th')]
                    writer.writerow(headers)
                
                for row in table.find('tbody').find_all('tr'):
                    data = [td.get_text(strip=True) for td in row.find_all('td')]
                    writer.writerow(data)
                print("Data for the current page extracted and saved to CSV.")
            else:
                print("Table not found.")

            # Check if there's a "Next" button and click it
            next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.Button.llwjsV'))) # Replace 'button.next-button-selector' with the actual selector for the "Next" button
            if next_button:
                next_button.click()
                time.sleep(5)  # Wait for the next set of rows to load
            else:
                print("No more pages left to scrape.")
                break
        except Exception as e:
            print(f"An error occurred: {e}")
            break

# Close the browser
driver.quit()

