from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from bs4 import BeautifulSoup
import pandas as pd
import time


# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(options=options)

# URL of the webpage with the search bar
url = 'https://www.fotmob.com/'
driver.get(url)
wait = WebDriverWait(driver, 25)

search_terms = ['Erling Haaland','Cole Palmer', 'Alexander Isak', 'Phil Foden']

for search_term in search_terms:
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
            main_div = divs[-1]

        imp_div = main_div.find('div') if outer_main else None  # Adjust this if nested <main> exists

        main_div = imp_div.find('div', class_="css-1gp959r-SeasonSelectCSS e105sp8f0") if outer_main else None  # Adjust this if nested <main> exists

        season_select = main_div.find('div') if outer_main else None  # Adjust this if nested <main> exists

        if season_select:
            select_tag = season_select.find('select') # Stores the select tag that has the dropdown to select different seasons

        if select_tag:
            aria_label = select_tag.get('aria-label') #, '')
            # Locate the select tag using Selenium
            select_element = driver.find_element(By.XPATH, f"//select[@aria-label='{select_tag.get('aria-label')}']")
            select_element.click()
            time.sleep(4)
            select = Select(select_element)

            if 'Premier League' not in aria_label:
                print("Selecting the correct option...")
             # Find and select the optgroup with the label '2023/2024'
                optgroup_2023_2024 = select_element.find_element(By.XPATH, ".//optgroup[@label='2023/2024']")
        
                # Inside this optgroup, find and click the option with the text 'Premier League'
                premier_league_option = optgroup_2023_2024.find_element(By.XPATH, ".//option[text()='Premier League']")
                premier_league_option.click()

                 # After the click, give the page some time to update the aria-label
                time.sleep(4)  # Adjust the sleep time if needed

                # Re-check the aria-label after the selection
                updated_aria_label = select_element.get_attribute('aria-label')
        
                if 'Premier League' in updated_aria_label:
                    print("Selection updated to 'Premier League'.")
                else:
                    print("Failed to update selection to 'Premier League'.")
        else:
            print("Correct selection already made: 'Premier League'.")

        ShotMapContainerCount = 0
        ShotMap18YCount =0
        ShotMap18Y2Count =0
        ShotMap18Y3Count =0
        ShotMap18Y4Count =0
        ShotMap18Y5Count = 0
    
    #except Exception as e:
    #    print(f"An error occurred with search term {search_term}: {e}")


        #Example: Extract text from a span
        ShotMapContainer = imp_div.find('div', class_="css-xgpjup-PlayerShotmapContainer e6kmgxk0")  # Adjust according to your target element
        
        if ShotMapContainer is None:
            ShotMapContainer = main_div.find_next_sibling('div')  # IT WORKS


        ShotMap18YBox = ShotMapContainer.find('div', class_='css-104gxio-ShotmapContainer eaj680o0')
            #soup.find('div', class_='css-2di36g-ShotmapAndStats eaj680o4')
        ShotMap18YBox2 = ShotMap18YBox.find('div', class_='css-2di36g-ShotmapAndStats eaj680o4')

        ShotMap18YBox3 = ShotMap18YBox2.find('div', class_="css-mxhuja-ShotmapTitleAndMap eaj680o2")

        ShotMap18YBox4 = ShotMap18YBox3.find('div', class_="css-15db3qs-TitleAndToggle eaj680o5")  # Adjust according to your target element

        ShotMap18YBox5 = ShotMap18YBox4.find('div', class_='css-169g342-ShotmapTitle eaj680o3')
       
        Span = ShotMap18YBox5.findChildren()[-1]
        if Span is not None:
            print('This is the span:', Span)
        else:
            Span = ShotMap18YBox5.find_all(recursive=False)[-1]
            print('This is the span:', Span)

        # Increment counts if any are missing
        ShotMapContainerCount += 1 if ShotMapContainer is None else 0
        ShotMap18YCount += 1 if ShotMap18YBox is None else 0
        ShotMap18Y2Count += 1 if ShotMap18YBox2 is None else 0
        ShotMap18Y3Count += 1 if ShotMap18YBox3 is None else 0
        ShotMap18Y4Count += 1 if ShotMap18YBox4 is None else 0
        ShotMap18Y5Count += 1 if ShotMap18YBox5 is None else 0


        # Print results for debugging
        print(f"{search_term} - ShotMapContainer missing: {ShotMapContainerCount}")
        print(f"{search_term} - ShotMap18YBox missing: {ShotMap18YCount}")
        print(f"{search_term} - ShotMap18YBox2 missing: {ShotMap18Y2Count}")
        print(f"{search_term} - ShotMap18YBox3 missing: {ShotMap18Y3Count}")
        print(f"{search_term} - ShotMap18YBox4 missing: {ShotMap18Y4Count}")
        print(f"{search_term} - ShotMap18YBox5 missing: {ShotMap18Y5Count}")
        
    except Exception as e:
        print(f"Error encountered: {str(e)}")
        #Save the extracted information (you can also write to a CSV)
       # print(f"Extracted info for {search_term}: {desired_info}")

        #Go back to the search page for the next term
       # driver.back()
        
       # print("Premier league already selected ")
        # Optional: Refresh or navigate back to reset the page state
   # driver.refresh()  # Refresh the page before the next search term
        time.sleep(5)  # Ensure the page has fully reloaded
        # Close the browser


    except Exception as e:
        print(f"An error occurred with search term {search_term}: {e}")

driver.quit()
