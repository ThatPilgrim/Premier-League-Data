from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import pandas as pd
import time

# Read the CSV file
csv_file = 'SofaScoreResults23-24.csv'
df = pd.read_csv(csv_file)

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(options=options)

# URL of the webpage with the search bar
url = 'https://www.fotmob.com/'
driver.get(url)
wait = WebDriverWait(driver, 10)

for search_term in df['Name']:  # Replace 'search_column' with your CSV column name
    try:
        # Locate and fill the search bar
        search_bar = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input.css-yevy7y-SearchInput.e1w60hxr4')))  # Adjust selector
        search_bar.clear()
        search_bar.send_keys(search_term)
        search_bar.send_keys(Keys.RETURN)

        # Wait for search results to load and click the first result
        first_result = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.css-1quojz0-SearchBoxItemCSS.e1kf1pm00')))  # Adjust selector
        first_result.click()

        # Parse the new page and extract information
        time.sleep(5)  # Wait for the page to load
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Wait for the select tag to be present
        select_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select.css-1211vxx-Select.eoq8rcw0')))
        
        # Find the optgroup with label '2023/2024'
        optgroup = select_element.find_element(By.XPATH, ".//optgroup[@label='2023/2024']")

        option = optgroup.find_element(By.XPATH, ".//option[@text()='Premier League']")
        option.click()
        print(f"Successfully selected the '{option.text}' option.")

        # try:
        #     # Check for the presence of the optgroup with the label '2024'
        #     try:
        #         optgroup_2024 = select_element.find_element(By.XPATH, ".//optgroup[@label='2024']")
        #         has_2024 = True
        #     except NoSuchElementException:
        #         has_2024 = False
    
        # # Based on the presence of '2024', select the appropriate option from '2023/2024'
        #     optgroup_2023_2024 = select_element.find_element(By.XPATH, ".//optgroup[@label='2023/2024']")
    
        #     option_value_prefix = '1' if has_2024 else '0'
        #     option = optgroup_2023_2024.find_element(By.XPATH, f".//option[starts-with(@value, '{option_value_prefix}')]")
        #     option.click()

        #     print(f"Successfully selected the '{option.text}' option.")
        # except NoSuchElementException as e:
        #     print(f"An error occurred with search term: {e}")












        # Continue with extracting the desired information
        # try:
        #     # Assuming you're now extracting other information from the page
        #     extracted_info = driver.find_element(By.XPATH, "//some_xpath").text
        #     print(f"Extracted information: {extracted_info}")
        # except Exception as e:
        #     print(f"An error occurred with search term {search_term}: {str(e)}")























        # # Print all options within the optgroup to verify their content
        # options = optgroup.find_elements(By.TAG_NAME, "option")
        # for option in options:
        #     print(f"Option value: {option.get_attribute('value')}, Option text: {option.text}")

        # # Now attempt to select the correct option
        # try:
        #     option = optgroup.find_element(By.XPATH, ".//option[@value='0-0']")  # or ".//option[text()='Premier League']"
        #     option.click()
        #     print("Successfully selected the 'Premier League' option.")
        # except Exception as e:
        #     print(f"Error selecting the option: {e}")




        # Select the option with value '1-0' or innerHTML 'Premier League'
        # option = select_element.find_element(By.XPATH, ".//option[@text()='Premier League']")  # or use .//option[text()='Premier League']
        # option.click()
        # WebDriverWait(driver, 10)


        # Example: Extract text from a span
        desired_info = soup.find('div', class_='css-169g342-ShotmapTitle.eaj680o3').text  # Adjust according to your target element

        desired_info = desired_info.find('span').text  # Adjust according to your target element

        # Save the extracted information (you can also write to a CSV)
        print(f"Extracted info for {search_term}: {desired_info}")

        # Go back to the search page for the next term
        driver.back()

    except Exception as e:
        print(f"An error occurred with search term {search_term}: {e}")

# Close the browser
driver.quit()
