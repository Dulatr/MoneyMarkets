import scrapy

class cnnMarket(scrapy.Spider):
    name="stocks"
    start_urls=[
        "https://money.cnn.com/data/markets/",
    ]

    def parse(self,response):
        for item in response.css("a.ticker"):
            yield {
                "Name": item.css('span.ticker-name::text').get(),
                "Points": item.css('span.ticker-points::text').get(),
                "Change": item.css('span.ticker-name-change span.posData::text').get(),
            }