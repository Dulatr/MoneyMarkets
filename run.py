from scrapy.crawler import CrawlerProcess
import os

filename = input("Please enter a filename for the spider output:> ")
if os.path.exists(filename):
    check = input("Data file path already exists, scrapy will currently only append. Do you wish to rename? (y/n):> ")
    if check in ('y','Y','yes','Yes'):
        filename = input("Please enter a filename for the spider output:> ")
    else:
        os.remove(filename)

process = CrawlerProcess(settings={
    "FEEDS": {
        filename: {"format": "json"},
    },
})

process.crawl(cnnMarket)
process.start()
