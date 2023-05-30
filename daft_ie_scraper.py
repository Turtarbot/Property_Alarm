from datetime import datetime
import asyncio

from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from tinydb import Query

from alarm import sound_alarm

timestamp_format = '%Y%m%d %H:%M:%S'


def scrape(webdriver, search_address, database, chat_id):
    webdriver.get(search_address)
    result_list_xpath = '//*[@id="__next"]/main/div[3]/div[1]/ul'
    result_list = webdriver.find_element(By.XPATH, result_list_xpath)
    # print(result_list.text)
    results = result_list.find_elements(By.CSS_SELECTOR, 'li')

    added_listings = 0
    for result in results:
        attempts = 0
        property_listing = {
            'link': '',
            'price': '',
            'address': '',
            'type': ''
        }
        errors = ""
        error_occurred = False
        while attempts < 5:
            error_occurred = False
            try:
                link = result.find_element(By.CSS_SELECTOR, 'a')
                property_listing['link'] = link.get_property("href")
            except WebDriverException as e:
                errors += e.msg + '\n'
                error_occurred = True
            try:
                info = result.find_element(By.CSS_SELECTOR, 'div[data-testid="title-block"]')
            except WebDriverException as e:
                errors += e.msg + '\n'
                error_occurred = True
            else:
                try:
                    price = info.find_element(By.CSS_SELECTOR, 'div[data-testid="price"]')
                    property_listing['price'] = price.text.replace('\u20ac', '')
                except WebDriverException as e:
                    errors += e.msg + '\n'
                    error_occurred = True
                try:
                    address = info.find_element(By.CSS_SELECTOR, 'h2[data-testid="address"]')
                    property_listing['address'] = address.text
                except WebDriverException as e:
                    errors += e.msg + '\n'
                    error_occurred = True
                try:
                    property_type = info.find_element(By.CSS_SELECTOR, 'div[data-testid="card-info"]')
                    property_listing['type'] = property_type.text.replace('\n', ' ')
                except WebDriverException as e:
                    errors += e.msg + '\n'
                    error_occurred = True
            if not error_occurred:
                break
            attempts += 1
        property_listing['time'] = datetime.now().strftime(timestamp_format)

        entries = Query()
        if error_occurred:
            print(errors)
        elif not database.contains(entries.link == property_listing['link']):
            database.insert(property_listing)
            added_listings += 1
            asyncio.run(sound_alarm(property_listing, chat_id))
    print("added " + str(added_listings))
4