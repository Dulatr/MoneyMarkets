import os
import sys
import json

from app import Stock
from utils.Parser import Parse

from multiprocessing import Queue
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
if args.app == 'stock':
    app = Stock(driver)
else:
    raise NotImplementedError(f"Application '{args.app}' not currently implemented in this version.")

app.Start()

data = {}

if args.overview:
    data["overview"] = app.getOverview()
if args.keystats:
    data["dow30"] = app.getTable()

data["last-updated"] = app.getUpdated()

app.Close()

cwd = os.getcwd()

if args.suppress:
    if not(os.path.exists("data")):
        os.makedirs('data')

    with open(cwd + f"/data/{args.app}.json",'w') as file:
        json.dump(data,file) 

else:
    sys.stdout.write(f"{data}")
