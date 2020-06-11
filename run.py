import os
import json

from selenium import webdriver
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
overview_data = {}
driver.get("https://money.cnn.com/data/markets/")
overview_items = driver.find_element_by_class_name("markets-overview")
tickers = overview_items.find_elements_by_css_selector("a.ticker")

for item in tickers:
    name=item.find_element_by_class_name("ticker-name").get_attribute('innerText')
    percent=item.find_element_by_class_name("ticker-name-change").text
    pts=item.find_element_by_class_name("ticker-points").text
    pts_change=item.find_element_by_class_name("ticker-points-change").text
    overview_data[name] = [pts,percent,pts_change]

DOW_composite_data ={}
driver.get("https://money.cnn.com/data/dow30/")
dow30_table = driver.find_element_by_css_selector('table.wsod_dataTableBig')
dow30_items = dow30_table.find_elements_by_tag_name('tr')

for item in dow30_items:
    name = item.find_element_by_class_name('wsod_firstCol').get_attribute('innerText').split('\xa0')[0]
    data = [txt.text for txt in item.find_elements_by_class_name("wsod_aRight")]
    DOW_composite_data[name] = data

driver.close()

cwd = os.getcwd()

with open(cwd + "/data/market_overview.json",'w') as file:
    json.dump(overview_data,file)  
with open(cwd + "/data/DOW30.json",'w') as file:
    json.dump(DOW_composite_data,file)
n):> ") in ('y','Y',"yes","Yes"):
        pass

