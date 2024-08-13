from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4.element import Tag    # For referencing BeautifulSoup's Tag class
import traceback
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, ElementClickInterceptedException, NoSuchElementException
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains


# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(options=options)

# URL of the webpage with the search bar
url = 'https://www.fotmob.com/'
driver.get(url)
wait = WebDriverWait(driver, 35)
def ColePalmer(driver, select_aria_label="Selected: EURO", desired_label="2023/2024", desired_value="1-0"):
    try:
        # Locate the select element based on the current aria-label
        select_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f"select[aria-label^='Selected: {select_aria_label}']"))
        )
        # Scroll the element into view and click using JavaScript
        driver.execute_script("arguments[0].scrollIntoView(true);", select_element)
        time.sleep(1)  # Allow time for any scroll action to complete
        driver.execute_script("arguments[0].click();", select_element)

        # Wait for the dropdown to be interactable
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'optgroup'))
        )

        # Find all optgroups
        optgroups = select_element.find_elements(By.TAG_NAME, 'optgroup')
        correct_optgroup = None

        for optgroup in optgroups:
            if optgroup.get_attribute("label") == desired_label:
                correct_optgroup = optgroup
                break

        if correct_optgroup:
            options = correct_optgroup.find_elements(By.TAG_NAME, 'option')
            correct_option = None

            for option in options:
                if option.get_attribute("value") == desired_value or option.text == "Premier League":
                    correct_option = option
                    break

            if correct_option:
                # Scroll into view and click
                driver.execute_script("arguments[0].scrollIntoView(true);", correct_option)
                time.sleep(1)
                correct_option.click()
                print("Correct option selected in optgroup.")
            else:
                print("Correct option not found in optgroup.")
        else:
            print("Correct optgroup not found.")

        # Wait for AJAX updates
        time.sleep(3)

        try:
            updated_select_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "select[aria-label^='Selected: Premier League']"))
            )
            selected_option_text = driver.execute_script("""
                let select = arguments[0];
                return select.options[select.selectedIndex].text;
            """, updated_select_element)
            print(f"Currently selected option: {selected_option_text}")
            
            if selected_option_text == "Premier League":
                print("Premier League is successfully selected.")
            else:
                print("The correct option is not selected.")
        except NoSuchElementException:
            print("Selected option not found.")
    except Exception as e:
        print(f"Error in select_option: {str(e)}")
    except ElementClickInterceptedException as e:
        print(f"Error in select_option: Element click intercepted: {str(e)}")

def NormalExecution(select_tag):
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


                    main_div_click = driver.find_element(By.CLASS_NAME, "css-1gp959r-SeasonSelectCSS.e105sp8f0")
                    main_div_click.click()
                    # Re-check the aria-label after the selection
                    updated_aria_label = select_element.get_attribute('aria-label')
            
                    if 'Premier League' not in updated_aria_label:
                        print("Selection reverted. Reselecting 'Premier League'...")
                        # Re-select the correct option
                        premier_league_option.click()
                        time.sleep(4)
                        updated_aria_label = select_element.get_attribute('aria-label')
                        if 'Premier League' not in updated_aria_label:
                            print("Failed to maintain 'Premier League' selection.")

                    elif 'Premier League' in updated_aria_label:
                        print("Selection updated to 'Premier League'.")
                        # Convert main_div to a WebDriver object and click it
                        main_div_click = driver.find_element(By.CLASS_NAME, "css-1gp959r-SeasonSelectCSS.e105sp8f0")
                        time.sleep(4)  # Add a short delay after clicking main_div
                        main_div_click.click()
                        print('Main div clicked.')
                    else:
                        print("Failed to update selection to 'Premier League'.")
                else:
                    print("Correct selection already made: 'Premier League'.")


search_tems = ['Erling Haaland','Cole Palmer', 'Alexander Isak', 'Phil Foden']
search_terms = ['Cole Palmer']
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
            plain_div = divs[-1]

        imp_div = plain_div.find('div') if outer_main else None  # Adjust this if nested <main> exists

        main_div = imp_div.find('div', class_="css-1gp959r-SeasonSelectCSS e105sp8f0") if outer_main else None  # Adjust this if nested <main> exists

        season_select = main_div.find('div') if outer_main else None  # Adjust this if nested <main> exists

        if season_select:
            select_tag = season_select.find('select') # Stores the select tag that has the dropdown to select different seasons
                            
######################### METHOD CALL IS HERE ##################################################


        if search_term == 'Cole Palmer':
            # Define any optional arguments if needed
            select_aria_label = "EURO"
            desired_label = "2023/2024"
            desired_value = "1-0"
            ColePalmer(driver,select_aria_label,desired_label, desired_value)
        else:
            NormalExecution(select_tag)

     
################################################################################################################################################################
# # FIND THE SHOT MAP ACCURACY
#         ShotMapContainerCount = 0
#         ShotMap18YCount =0
#         ShotMap18Y2Count =0
#         ShotMap18Y3Count =0
#         ShotMap18Y4Count =0
#         ShotMap18Y5Count = 0
    
#         main_div = driver.find_element(By.CLASS_NAME, "css-1gp959r-SeasonSelectCSS.e105sp8f0")

# # Replace find_next_sibling with Selenium's find_element using XPath to locate the sibling div
#         ShotMapContainer = main_div.find_element(By.XPATH, "./following-sibling::div")

# # Handling potential stale element error
#         try:
#     # Locate ShotMap18YBox inside ShotMapContainer
#             ShotMap18YBox = ShotMapContainer.find_element(By.CLASS_NAME, 'css-104gxio-ShotmapContainer.eaj680o0')
#         except StaleElementReferenceException:
#         # If a stale element error occurs, relocate ShotMapContainer and try again
#             ShotMapContainer = driver.find_element(By.XPATH, "./following-sibling::div")
#             ShotMap18YBox = ShotMapContainer.find_element(By.CLASS_NAME, 'css-104gxio-ShotmapContainer.eaj680o0')

# # Now proceed to find the other elements inside ShotMap18YBox using Selenium's methods
#         ShotMap18YBox2 = ShotMap18YBox.find_element(By.CLASS_NAME, 'css-2di36g-ShotmapAndStats.eaj680o4')
#         ShotMap18YBox3 = ShotMap18YBox2.find_element(By.CLASS_NAME, 'css-mxhuja-ShotmapTitleAndMap.eaj680o2')
#         ShotMap18YBox4 = ShotMap18YBox3.find_element(By.CLASS_NAME, 'css-15db3qs-TitleAndToggle.eaj680o5')
#         ShotMap18YBox5 = ShotMap18YBox4.find_element(By.CLASS_NAME, 'css-169g342-ShotmapTitle.eaj680o3')

# # Locate the last child (span) within ShotMap18YBox5
#         try:
#             children = ShotMap18YBox5.find_elements(By.XPATH, './*')
#             Span = children[-1] if children else None
    
#             if Span is not None:
#                 span_text = Span.text
#                 if ':' in span_text:
#                     number_after_colon = span_text.split(':')[1].strip()  # Extract and trim the number
#                     print('Number after colon:', number_after_colon)
#             #else:
#                 # Attempt to locate using another method
#              #   Span = ShotMap18YBox5.find_elements(By.XPATH, './*')[-1]
#               #  print('2This is the span:', Span)

#         except IndexError:
#             print("No children found in ShotMap18YBox5.")

#         # Increment counts if any are missing
#         ShotMapContainerCount += 1 if ShotMapContainer is None else 0
#         ShotMap18YCount += 1 if ShotMap18YBox is None else 0
#         ShotMap18Y2Count += 1 if ShotMap18YBox2 is None else 0
#         ShotMap18Y3Count += 1 if ShotMap18YBox3 is None else 0
#         ShotMap18Y4Count += 1 if ShotMap18YBox4 is None else 0
#         ShotMap18Y5Count += 1 if ShotMap18YBox5 is None else 0

#         # Print results for debugging
#         print(f"{search_term} - ShotMapContainer missing: {ShotMapContainerCount}")
#         print(f"{search_term} - ShotMap18YBox missing: {ShotMap18YCount}")
#         print(f"{search_term} - ShotMap18YBox2 missing: {ShotMap18Y2Count}")
#         print(f"{search_term} - ShotMap18YBox3 missing: {ShotMap18Y3Count}")
#         print(f"{search_term} - ShotMap18YBox4 missing: {ShotMap18Y4Count}")
#         print(f"{search_term} - ShotMap18YBox5 missing: {ShotMap18Y5Count}")

    

# ################################################################################################################################################################
# # FIND THE SHOT'S IN BOX ETC (4 - 6)

#         ShotMapPostandFilter = ShotMap18YBox.find_element(By.CLASS_NAME, 'css-158vgtt-ShotInformationWrapper.eaj680o1')
#         ShotMapFilter = ShotMapPostandFilter.find_element(By.CLASS_NAME, 'css-yd9zf5-ShotFilters.e33hihm1')
#         ShotMapFilterContainer = ShotMapFilter.find_element(By.CLASS_NAME, 'css-527u5l-ShotFiltersContainer.e33hihm0')

#         # Find all buttons inside the ShotMapFilterContainer
#         buttons = ShotMapFilterContainer.find_elements(By.CLASS_NAME, 'css-5ig26z-ShotFilterButton.e33hihm2')

#         # Define the statistics you are interested in
#         target_statistics = ["Regular play", "Shots inside box", "Shots outside box", "Penalty"]

#         for button in buttons:
#             spans = button.find_elements(By.TAG_NAME, 'span')
    
#             if len(spans) == 2:
#                 stat_name = spans[0].text
#                 stat_number = spans[1].text
        
#                 if stat_name in target_statistics:
#                     print(f"{stat_name}: {stat_number} for {search_term}")


################################################################################################################################################################
# FIND THE SHOT'S IN BOX ETC (23, 26-30)
        start_loop = 0
        Per90_loop = 0
        while start_loop <2:
            Empty_div = main_div.find_parent()


            # Ensure Empty_div is not None before proceeding
            if Empty_div is not None:
                try:
                    # Check if Empty_div is indeed a Selenium WebElement
                    print(f"Type of Empty_div: {type(Empty_div)}")

                    # Attempt to find all divs
                    #divs = Empty_div.find_elements(By.TAG_NAME, "div")
                    divs = Empty_div.find_all("div")

                   # Assume `divs` is a list of WebElement or Tag objects
                    for div in divs:
                        try:
                            # For Selenium WebElement
                            if isinstance(div, WebElement):
                                div_class = div.get_attribute('class')
                                print(f"Div class: {div_class}")

                            # For BeautifulSoup Tag
                            elif isinstance(div, Tag):
                                div_class = div.get("class")
                                print(f"Div class: {div_class}")

                        except AttributeError as e:
                            print(f"AttributeError occurred: {e}")

                        except Exception as e:
                            print(f"An unexpected error occurred: {e}")

                except Exception as e:
                    print(f"An error occurred: {e}")
            else:
                print("Empty_div is None. Cannot proceed with finding elements.")

            # Then, find the 'SeasonPerformanceCSS' div
            SeasonPerformance = Empty_div.find("div", class_="css-15lw8xy-SeasonPerformanceCSS e1uibvo19")

            # Proceed with the rest of your code
            SeasonPerformanceHeader = SeasonPerformance.find("div", class_="css-1f7ec8g-SeasonPerformanceHeader e1uibvo112")
            SeasonPerformanceHeaderRight = SeasonPerformanceHeader.find("div", class_="css-12ltoon-FilterButtonsContainer e1aie6870")
            Per90Button_soup = SeasonPerformanceHeaderRight.find("button", string="Per 90")
            if Per90_loop == 1:
                if Per90Button_soup:
                # Convert the found element to a Selenium WebElement by its text
                    Per90Button = driver.find_element(By.XPATH, f"//button[text()='{Per90Button_soup.text}']")

                
                    try:
                        # Scroll the button into view
                        driver.execute_script("arguments[0].scrollIntoView(true);", Per90Button)

                        # Additional wait to ensure any other elements are out of the way
                        time.sleep(1)

                        # Attempt to click using JavaScript if necessary
                        driver.execute_script("arguments[0].click();", Per90Button)

                        time.sleep(1)  # Give time for any actions to complete
                        active_button_class = "css-vgq3an-FilterButton e1aie6871"
                        active_button = driver.find_element(By.XPATH, f"//button[contains(@class, '{active_button_class}')]")

                        if active_button.text == "Per 90":
                            print("Per 90 button is successfully selected.")
                        else:
                            raise Exception("Per 90 button did not remain selected.")
            
                        time.sleep(3)  # Allow time for the content to update

                    except Exception as e:
                        print(f"Error encountered: {str(e)}", traceback.format_exc())

                else:
                    raise Exception("Per 90 button not found in the DOM")


    # Re-fetch the updated page source after the click
            updated_html = driver.page_source
            soup = BeautifulSoup(updated_html, 'html.parser')
            new_main_div = soup.find('div', class_='css-1gp959r-SeasonSelectCSS e105sp8f0')
            Empty_div = new_main_div.find_parent()

            # Then, find the 'SeasonPerformanceCSS' div
            SeasonPerformance = Empty_div.find("div", class_="css-15lw8xy-SeasonPerformanceCSS e1uibvo19")

            # Proceed with the rest of your code
            SeasonPerformanceHeader = SeasonPerformance.find("div", class_="css-1f7ec8g-SeasonPerformanceHeader e1uibvo112")

            DetailedStats = SeasonPerformanceHeader.find_next_sibling()

            # Wait for the Per90Button to be present and clickable
            try:
                # Get all relevant div elements initially
                stat_items = DetailedStats.find_all('div', class_="css-1v73fp6-StatItemCSS e1uibvo10")
        
                # List of specific stat_names you're interested in
                desired_stats2 = ['Goals','Expected goals (xG)','xG on target (xGOT)', 'Shots', 'Shots on target', 'Pass accuracy','Dribble success', 'Touches', 'Touches in opposition box']

            # Loop through each stat_item div
                for stat_item in stat_items:
            # Find the stat name in the first inner div
                    stat_name_div = stat_item.find('div', class_="css-2duihq-StatTitle e1uibvo11")
            
                    if stat_name_div:
                        stat_name = stat_name_div.text.strip()

                # Only process if stat_name is in desired_stats2
                        if stat_name in desired_stats2:
                    # Find the first nested div with the stat value span
                            stat_value_div = stat_item.find('div', class_="css-17zw5kc-StatCSS e1uibvo13")
                    
                            if stat_value_div:
                                stat_value_span = stat_value_div.find('span')
                        
                                if stat_value_span:
                                    stat_value = stat_value_span.text.strip()
                                    print(f"{stat_name}: {stat_value}")
                                else:
                                    print(f"Error: Could not find span for {stat_name}")
                            else:
                                print(f"Error: Could not find value div for {stat_name}")
                        #else:
                        #    print(f"Skipped {stat_name} as it is not in the desired list.")
                    else:
                        print("Error: Could not find stat name div.")
            except Exception as e:
                print(f"Error encountered while retrieving stats: {str(e)}")
            Per90_loop =Per90_loop+1
            start_loop=start_loop+1


















        # Example usage
        # driver = webdriver.Chrome() # or any other browser you are using
        # driver.get("https://www.fotmob.com/players/1096353/cole-palmer") # Example player page
        # select_option(driver, select_aria_label="EURO")






























# Continue with Selenium from here
        # try:
        #     loop_starter = 1 # variable to ensure stat_items is assigned to DetailedStats just once.
        #     if loop_starter > 0:
        #         stat_items = DetailedStats.find('div', "css-1v73fp6-StatItemCSS e1uibvo10")
        #         loop_starter = 0

        #     desired_stats2 = ['xG on target (xGOT)','Shots', 'Shots on target', 'Dribble success', 'Touches', 'Touches in opposition box']
        #     stat_starter = 0 # Counter to ensure stat_items is assigned to its next sibling after the second time the while loop runs

        #     # While loop to ensure that stat_items is only a div or a header so that it terminates once it isn't either of them.
        #     while stat_items.find_next_sibling('div', class_='css-1v73fp6-StatItemCSS e1uibvo10') or stat_items.find_next_sibling('h3', class_='css-lssgg4-StatGroupTitle e1uibvo14'):

        #         if stat_starter > 0:
        #             stat_items = stat_items.find_next_sibling('div', class_='css-1v73fp6-StatItemCSS e1uibvo10')

        #         if stat_items.name != 'div':
        #             print('A header was found')
        #             break # this break is supposed to end the while loop

                 
        #         for stat_item in stat_items:
        #       #  stat_name_div = stat_item.find('div', "css-2duihq-StatTitle e1uibvo11")
        #             stat_name = stat_item.text

        #             if stat_name in desired_stats2:
        #                 stat_value_div = stat_item.find_next_sibling('div')
        #      #   stat_value_span = stat_value_div.find('div', class_='div.css-jb6lgd-StatValue e1uibvo12')
        #                 stat_value_span = stat_value_div.find('span')
        #                 stat_value = stat_value_span.text
        #                 print(f"{stat_name}: {stat_value}")
        #             else:
        #                 print(f"Skipped {stat_name} as it is not in the desired list.")
        #         stat_starter= stat_starter+1
        # except Exception as e:
        #     print(f"Error encountered while retrieving stats: {str(e)}")

    
    except Exception as e:
        print(f"Error encountered: {str(e)}")



























    #except Exception as e:
    #    print(f"An error occurred with search term {search_term}: {e}")


        #Example: Extract text from a span
        #ShotMapContainer = imp_div.find('div', class_="css-xgpjup-PlayerShotmapContainer e6kmgxk0")  # Adjust according to your target element
        
    #    # if ShotMapContainer is None:
    #     main_div = driver.find_element(By.CLASS_NAME, "css-1gp959r-SeasonSelectCSS.e105sp8f0")

    #     ShotMapContainer = main_div.find_next_sibling('div')  # IT WORKS


    #    # ShotMap18YBox = ShotMapContainer.find('div', class_='css-104gxio-ShotmapContainer eaj680o0')
    #         #soup.find('div', class_='css-2di36g-ShotmapAndStats eaj680o4')

    #          # Handling stale element error by re-locating ShotMapContainer if needed
    #     try:
    #         ShotMap18YBox = ShotMapContainer.find('div', class_='css-104gxio-ShotmapContainer eaj680o0')
    #     except StaleElementReferenceException:
    #         ShotMapContainer = driver.find_element(By.CLASS_NAME, "css-1gp959r-SeasonSelectCSS e105sp8f0")
    #         ShotMap18YBox = ShotMapContainer.find_element(By.CLASS_NAME, 'css-104gxio-ShotmapContainer eaj680o0')

    #     ShotMap18YBox2 = ShotMap18YBox.find('div', class_='css-2di36g-ShotmapAndStats eaj680o4')

    #     ShotMap18YBox3 = ShotMap18YBox2.find('div', class_="css-mxhuja-ShotmapTitleAndMap eaj680o2")

    #     ShotMap18YBox4 = ShotMap18YBox3.find('div', class_="css-15db3qs-TitleAndToggle eaj680o5")  # Adjust according to your target element

    #     ShotMap18YBox5 = ShotMap18YBox4.find('div', class_='css-169g342-ShotmapTitle eaj680o3')
       
    #     Span = ShotMap18YBox5.findChildren()[-1]
    #     if Span is not None:
    #         print('This is the span:', Span)
    #     else:
    #         Span = ShotMap18YBox5.find_all(recursive=False)[-1]
    #         print('This is the span:', Span)

    #     # Increment counts if any are missing
    #     ShotMapContainerCount += 1 if ShotMapContainer is None else 0
    #     ShotMap18YCount += 1 if ShotMap18YBox is None else 0
    #     ShotMap18Y2Count += 1 if ShotMap18YBox2 is None else 0
    #     ShotMap18Y3Count += 1 if ShotMap18YBox3 is None else 0
    #     ShotMap18Y4Count += 1 if ShotMap18YBox4 is None else 0
    #     ShotMap18Y5Count += 1 if ShotMap18YBox5 is None else 0


    #     # Print results for debugging
    #     print(f"{search_term} - ShotMapContainer missing: {ShotMapContainerCount}")
    #     print(f"{search_term} - ShotMap18YBox missing: {ShotMap18YCount}")
    #     print(f"{search_term} - ShotMap18YBox2 missing: {ShotMap18Y2Count}")
    #     print(f"{search_term} - ShotMap18YBox3 missing: {ShotMap18Y3Count}")
    #     print(f"{search_term} - ShotMap18YBox4 missing: {ShotMap18Y4Count}")
    #     print(f"{search_term} - ShotMap18YBox5 missing: {ShotMap18Y5Count}")
        
    # except Exception as e:
    #     print(f"Error encountered: {str(e)}")
        #Save the extracted information (you can also write to a CSV)
       # print(f"Extracted info for {search_term}: {desired_info}")

        #Go back to the search page for the next term
       # driver.back()
        
       # print("Premier league already selected ")
        # Optional: Refresh or navigate back to reset the page state
   # driver.refresh()  # Refresh the page before the next search term
    #    time.sleep(5)  # Ensure the page has fully reloaded
        # Close the browser


    #except Exception as e:
     #   print(f"An error occurred with search term {search_term}: {e}")

driver.quit()
