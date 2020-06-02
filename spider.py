import scrapy

class cnnMarket(scrapy.Spider):
    name="money.cnn"
    start_urls=[
        "https://money.cnn.com/data/markets/",
    ]

    def parse(self,response):
        if response.url == self.start_urls[0]:
            for item in response.css("a.ticker"):
                yield {
                    "Name": item.css('span.ticker-name::text').get(),
                    "Points": item.css('span.ticker-points::text').get(),
                    "Change": item.css('span.ticker-name-change span.posData::text').get(),
                }
        else:
            for item in response.css("tr"):
                ticker = item.css("td.wsod_firstCol span::text").get()
                if ticker is not None:
                    yield {
                        "name":ticker,
                        "price_data":item.css("td.wsod_aRight span::text").getall(),
                    }    
        
        next_page = response.css("a.module-header::attr(href)").getall()
        
        for item in next_page:
            new_page = response.urljoin(item)
            yield scrapy.Request(new_page,callback=self.parse)