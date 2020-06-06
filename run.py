import os
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

try:
    DRIVER = os.environ['SELENIUM_CHROME']
except KeyError:
    print("No SELENIUM_CHROME env variable set. Please set this to your webdriver.")
    print("Exiting...")
    exit(1)

# Setup headless browser options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("log-level=3")
chrome_options.add_experimental_option("prefs",{"profile.default_content_settings.cookies": 2})
driver = webdriver.Chrome(executable_path="{}/chromedriver.exe".format(DRIVER),options=chrome_options)

# Visit and retreive info from page
driver.get("https://money.cnn.com/data/markets/")
overview_items = driver.find_element_by_class_name("markets-overview")
tickers = overview_items.find_elements_by_css_selector("a.ticker")

ticker_data = {}

for item in tickers:
    name=item.find_element_by_class_name("ticker-name").get_attribute('innerText')
    percent=item.find_element_by_class_name("ticker-name-change").text
    pts=item.find_element_by_class_name("ticker-points").text
    pts_change=item.find_element_by_class_name("ticker-points-change").text
    ticker_data[name] = [pts,percent,pts_change]

driver.close()

if not os.path.exists(os.getcwd() + "/data/market_overview.json"):
    with open(os.getcwd() + "/data/market_overview.json",'w') as file:
        json.dump(ticker_data,file)
else:
    if input("Data file exists, do you wish to overwrite? (y/n):> ") in ('y','Y',"yes","Yes"):
        pass
