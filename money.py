import os
import json

from app import Stock
from utils.Parser import Parse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

args = Parse()

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
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_experimental_option("prefs",{"profile.default_content_settings.cookies": 2})
driver = webdriver.Chrome(executable_path="{}/chromedriver.exe".format(DRIVER),options=chrome_options)

# Get stock info by default
app = Stock(driver)

app.Start()
overview_data = app.getOverview()
DOW_composite_data = app.getTable()
app.Close()

cwd = os.getcwd()

if args.suppress:
    with open(cwd + "/data/market_overview.json",'w') as file:
        json.dump(overview_data,file) 

    with open(cwd + "/data/DOW30.json",'w') as file:
        json.dump(DOW_composite_data,file)
else:
    print(f"{overview_data}\n{DOW_composite_data}")
