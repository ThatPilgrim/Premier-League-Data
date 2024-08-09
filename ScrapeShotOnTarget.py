
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
url = 'https://www.premierleague.com/stats/top/players/ontarget_scoring_att'
driver.get(url)

# Increase wait time if necessary
wait = WebDriverWait(driver, 45)  # Waits up to 45 seconds

    # Handle cookie consent banner if present
cookie_button = wait.until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
cookie_button.click()
time.sleep(2)  # Allow time for the banner to close

# Make the dropdown selection
dropdown = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.current'))) # Replace with the correct dropdown selector
dropdown.click()
time.sleep(5)  # Add a small delay to allow the dropdown to load options

# Select the appropriate option from the dropdown
#option = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'your-option-selector'))) # Replace with the correct option selector
#option.click()
#time.sleep(3)  # Wait for the table to load

# Open the CSV file in append mode
with open(r'C:\Users\manny\Documents\SofaScoreLiveRating\table_data.csv', 'a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    rows_extracted = 0

    while rows_extracted < 50:
        try:
            # Wait for the table to be present on the page
            table_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.table.statsTable.stats-table table')))
            
            # Parse the page source with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # Locate the table
            outer_main = soup.find('main', id='mainContent')
            
            main_div = outer_main.find('div', class_ ='wrapper col-12') if outer_main else None  # Adjust this if nested <main> exists

            main_div = main_div.find('div') if outer_main else None  # Adjust this if nested <main> exists

            main_div = main_div.find('div', class_ = 'table statsTable stats-table') if outer_main else None  # Adjust this if nested <main> exists

            table = main_div.find('table') if outer_main else None  # Adjust this if nested <main> exists

            if table:
                if rows_extracted == 0:  # Write headers only on the first extraction
                    headers = [th.get_text(strip=True) for th in table.find('thead').find_all('th')]
                    writer.writerow(headers)
                
                for row in table.find('tbody').find_all('tr'):
                    data = [td.get_text(strip=True) for td in row.find_all('td')]
                    writer.writerow(data)
                    rows_extracted += 1
                    if rows_extracted >= 40:
                        break
                print(f"Extracted {rows_extracted} rows so far.")
            else:
                print("Table not found.")
                break

            # Check if there's a "Next" button and click it
            if rows_extracted < 50:
                next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.paginationBtn.paginationNextContainer')))
                next_button.click()
                time.sleep(5)  # Wait for the next set of rows to load
            else:
                print("Desired number of rows extracted.")
                break
        except Exception as e:
            print(f"An error occurred: {e}")
            break

# Close the browser
driver.quit()


#                 if file.tell() != 0:  # Check if the file is empty to write headers
#                     headers = [th.get_text(strip=True) for th in table.find('thead').find_all('th')]
#                     writer.writerow(headers)
                
#                 for row in table.find('tbody').find_all('tr'):
#                     data = [td.get_text(strip=True) for td in row.find_all('td')]
#                     writer.writerow(data)
#                 print("Data for the current page extracted and saved to CSV.")
#             else:
#                 print("Table not found.")

#             # Check if there's a "Next" button and click it
#             next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.paginationBtn paginationNextContainer'))) # Replace 'button.next-button-selector' with the actual selector for the "Next" button
#             if next_button:
#                 next_button.click()
#                 time.sleep(5)  # Wait for the next set of rows to load
#             else:
#                 print("No more pages left to scrape.")
#                 break
#         except Exception as e:
#             print(f"An error occurred: {e}")
#             break

# # Close the browser
# driver.quit()

