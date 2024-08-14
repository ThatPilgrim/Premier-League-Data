import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(options=options)

csv_file = 'SofaScoreResults23-24.csv'
df = pd.read_csv(csv_file)

# URL of the webpage with the search bar
url = 'https://www.fotmob.com/'
driver.get(url)
wait = WebDriverWait(driver, 35)


for search_term in df['Name']:
    try:
             
        # Refresh the page to ensure a clean state
        driver.refresh()
        time.sleep(5)  # Give time for the page to reload

        # Clear the search bar and enter a new search term
        search_bar = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input.css-yevy7y-SearchInput.e1w60hxr4')))
        search_bar.clear()
        search_bar.send_keys(search_term)
        search_bar.send_keys(Keys.RETURN)

        # Click the first result
        first_result = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.css-1quojz0-SearchBoxItemCSS.e1kf1pm00')))
        first_result.click()

        # Wait for the URL to update
        time.sleep(5)
        current_url = driver.current_url
        print(f"Current URL after clicking on {search_term}: {current_url}")

        # Verify the correct page loaded
        if search_term.lower().replace(" ", "-") in current_url:
            print(f"Correct player page loaded for {search_term}.")
        else:
            print(f"Incorrect player page loaded for {search_term}. Skipping further actions.")
            continue

        # Proceed with existing logic to find elements and interact with the page
        # ...
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        body = soup.find('body')
        first_div = body.find('div', id = '__next')

        outer_main = first_div.find('main', class_='css-1cyagd9-PageContainerStyles e19hkjx10')
        
        main_div = outer_main.find('main') if outer_main else None

        main_div = main_div.find('div', class_ ='css-17js6f6-PlayerPageGridCSS e17ysukt0') if outer_main else None  # Adjust this if nested <main> exists

        main_div = main_div.find('div', class_='css-9c39tl-Column-LeftColumnCSS e17ysukt1') if outer_main else None  # Adjust this if nested <main> exists

        divs = main_div.find_all('div', class_ = 'css-1wb2t24-CardCSS e1mlfzv61') if outer_main else None  # Adjust this if nested <main> exists
        
        if divs:
            plain_div = divs[-1]

        imp_div = plain_div.find('div') if outer_main else None  # Adjust this if nested <main> exists

        minutes_div = imp_div.find('div', 'css-15lw8xy-SeasonPerformanceCSS e1uibvo19')

        SeasonPerformanceHeader = minutes_div.find('div', 'css-1f7ec8g-SeasonPerformanceHeader e1uibvo112')

        header = SeasonPerformanceHeader.find('h2', 'css-1gt9w1g-SeasonPerformanceTitle e1uibvo110')

        # Find the index of the colon
        colon_index = header.text.find(':')

        # Extract the substring that comes after the colon and strip any whitespace
        formatted_text = header.text[colon_index + 1:].strip()
        
        print('Minutes played: ',formatted_text)


     #   main_div = imp_div.find('div', class_="css-1gp959r-SeasonSelectCSS e105sp8f0") if outer_main else None  # Adjust this if nested <main> exists

      #  season_select = main_div.find('div') if outer_main else None  # Adjust this if nested <main> exists

      #  if season_select:
       #     select_tag = season_select.find('select') # Stores the select tag that has the dropdown to select different seasons
    except Exception as e:
        print(f"Error encountered: {str(e)}")