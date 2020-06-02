# Stock Quote Scraper

This script retrieves and stores the quoted prices for the DOW, Nasdaq and S&P 500 from the [CNN money markets](https://money.cnn.com/data/markets/). Retrieved data is stored in the JSON format for a file specified by the user prompt.

## Requirements

In it's current form, this project uses [scrapy](https://github.com/scrapy/scrapy) which has the following list of dependencies:

* [lxml](https://lxml.de/index.html)
* [parsel](https://pypi.org/project/parsel/)
* [w3lib](https://pypi.org/project/w3lib/)
* [twisted](https://twistedmatrix.com/trac/)
* [cryptography](https://cryptography.io/en/latest/)
* [pyOpenSSL](https://pypi.org/project/pyOpenSSL/)

Be aware that it's recommend scrapy is installed in a python [virtual environment](https://virtualenv.pypa.io/en/latest/) to prevent any issues with system files. If you want detail instructions on getting scrapy installed check out their [documentation pages](https://docs.scrapy.org/en/latest/intro/install.html). 

## Future changes

Since the way this project is setup, it was mainly a way for me to get introduced to scrapy and some of the parsing libraries for response data. I'll likely reduced the requirements to requests, lxml and parsel packages to achieve the same. I'd like to extend this script into a stock price package using these libraries that will be accessed on PyPi similar to how [googlefinance](https://pypi.org/project/googlefinance/) does it, but as a focus towards scraping the data rather than API access. 