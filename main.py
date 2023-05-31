from enum import Enum
from argparse import ArgumentParser

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from tinydb import TinyDB


class ScraperType(Enum):
    DAFT_IE = 0
    IMMOSCOUT_AT = 1
    WILLHABEN_AT = 2


parser = ArgumentParser(description='Property Scraper with Telegram Alarm Bot')

parser.add_argument('-c', '--chat-id', type=str, help='Chat ID of the Telegram Chat the new found Properties should '
                                                      'be sent to')
parser.add_argument('-t', '--scraper-type', type=int, help='Which Website do you want to search? \n0 - daft.ie\n1 - '
                                                           'immobilienscout24.at\n2 - willhaben.at')
parser.add_argument('-db', '--database-path', type=str, help='Path to the database you want to save the listings in. '
                                                             'A new database will be created at the specified path if'
                                                             ' it does not exist yet.')
parser.add_argument('-a', '--search-address', type=str, help='The full address of the property list you want to '
                                                             'search. e.g. "https://www.daft.ie/for-rent"')
args = parser.parse_args()

chat_id = args.chat_id
scraper_type = ScraperType(args.scraper_type)
db_path = args.database_path
search_address = args.search_address

if scraper_type is ScraperType.DAFT_IE:
    from daft_ie_scraper import scrape
elif scraper_type is ScraperType.WILLHABEN_AT:
    pass
elif scraper_type is ScraperType.IMMOSCOUT_AT:
    from immoscout_at_scraper import scrape
else:
    pass

db = TinyDB(db_path)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
chrome_options.add_argument('window-size=1200x600')

chrome_service = Service('./Chromedriver/chromedriver.exe')
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

try:
    scrape(driver, search_address, db, args.chat_id)
finally:
    driver.quit()
