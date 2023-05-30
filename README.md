# Property Scraper with Telegram Alarm Bot

This repository contains a property scraper tool with a Telegram alarm bot. The tool is designed to scrape property listings from property websites and send alarm notifications to a Telegram chat.

## Files

1. `main.py`: This file contains the main script for running the property scraper with the Telegram alarm bot. It accepts command-line arguments to configure the scraper and initiates the scraping process. The script uses the Selenium library to interact with web pages and the TinyDB library to store the scraped data.

2. `daft_ie_scraper.py`: This file contains the scraper module specific to the daft.ie website. It provides the necessary functions to scrape property listings from daft.ie and extract relevant information such as price, address, and property type.

3. `alarm.py`: This file contains the alarm module responsible for sending alarm notifications to a Telegram chat. It utilizes the Telegram Bot API and the `python-telegram-bot` library to send messages with property details to the specified chat.

## Usage

1. Install the required dependencies by running `pip install -r requirements.txt`.

2. Set up a Telegram Bot and obtain a Bot Token.

3. Update the `BOT_TOKEN` variable in the `alarm.py` file with your Telegram Bot Token.

4. Run the `main.py` script with appropriate command-line arguments to configure the scraper. For example:
   
   `python main.py -c <CHAT_ID> -t 0 -db listings.db -a "https://www.daft.ie/for-rent"`
   
   Replace `<CHAT_ID>` with the Chat ID of the Telegram chat where you want to receive alarm notifications. Choose the appropriate scraper type (`0` for daft.ie) and specify the path for the database file (`listings.db`) and the property search address.

5. The scraper will start scraping the property listings and send alarm notifications to the specified Telegram chat whenever a new listing is found.

