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

