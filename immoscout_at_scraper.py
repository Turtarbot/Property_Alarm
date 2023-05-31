from datetime import datetime
import asyncio

from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from tinydb import Query

from alarm import sound_alarm

# Define the format for the timestamp
timestamp_format = '%Y%m%d %H:%M:%S'


def scrape(webdriver, search_address, database, chat_id):
    # Open the provided search address in the WebDriver
    webdriver.get(search_address)

    # Find the result list element using its XPath
    result_list_xpath = '//*[@id="cope_ref"]/section[2]/ol'
    result_list = webdriver.find_element(By.XPATH, result_list_xpath)

    # Retrieve all the individual result items from the result list
    results = result_list.find_elements(By.CSS_SELECTOR, 'li')

    # Initialize a counter to keep track of added listings
    added_listings = 0

    for result in results:
        # Filter out ads
        if result.get_attribute("class") != "J04SL w-full":
            continue
        attempts = 0

        # Initialize a dictionary to store the listing details
        property_listing = {
            'link': '',
            'price': '',
            'address': '',
            'type': ''
        }

        # Initialize variables to track errors during scraping
        errors = ""
        error_occurred = False

        while attempts < 2:
            error_occurred = False

            try:
                # Retrieve the link element for the property listing
                link = result.find_element(By.CSS_SELECTOR, 'a')
                property_listing['link'] = link.get_property("href")
            except WebDriverException as e:
                errors += e.msg + '\n'
                error_occurred = True

            try:
                # Retrieve the information container for the property listing
                info = result.find_element(By.XPATH, './a/section/section[1]/ul')
            except WebDriverException as e:
                errors += e.msg + '\n'
                error_occurred = True
            else:
                try:
                    info_elements = info.find_elements(By.CSS_SELECTOR, 'li')
                    # Retrieve the price information for the property listing
                    price = info_elements.pop(-1)
                    property_listing['price'] = price.text.replace('\u20ac', '')
                    for info_element in info_elements:
                        property_listing['type'] += info_element.text + ' | '
                except WebDriverException as e:
                    errors += e.msg + '\n'
                    error_occurred = True

                try:
                    # Retrieve the address information for the property listing
                    address = result.find_element(By.CSS_SELECTOR, 'address')
                    property_listing['address'] = address.text
                except WebDriverException as e:
                    errors += e.msg + '\n'
                    error_occurred = True

            if not error_occurred:
                break

            attempts += 1

        # Add the timestamp to the property listing
        property_listing['time'] = datetime.now().strftime(timestamp_format)

        entries = Query()

        if error_occurred:
            # Print any errors that occurred during scraping
            print(errors)
        elif not database.contains(entries.link == property_listing['link']):
            # Insert the property listing into the database if it's not a duplicate
            database.insert(property_listing)
            added_listings += 1

            # Run the sound_alarm function asynchronously to trigger a notification
            asyncio.run(sound_alarm(property_listing, chat_id))

    # Print the number of added listings after the scraping is complete
    print("Added " + str(added_listings) + " listings")
