from selenium import webdriver

class Stock:

    def __init__(self,client: webdriver.Chrome,**kwargs):
        self._configuration = kwargs
        self._client = client
    
    def Start(self):
        self._client.get("https://money.cnn.com/data/markets/")
    
    def getOverview(self):
        overview_data = {}

        overview_items = self._client.find_element_by_class_name("markets-overview")
        tickers = overview_items.find_elements_by_css_selector("a.ticker")
        
        for item in tickers:
            name=item.find_element_by_class_name("ticker-name").get_attribute('innerText')
            percent=item.find_element_by_class_name("ticker-name-change").text
            pts=item.find_element_by_class_name("ticker-points").text
            pts_change=item.find_element_by_class_name("ticker-points-change").text
            overview_data[name] = [pts,percent,pts_change]
        
        return overview_data

    def getTable(self):
        DOW_composite_data ={}
        self._client.get("https://money.cnn.com/data/dow30/")
        dow30_table = self._client.find_element_by_css_selector('table.wsod_dataTableBig')
        dow30_items = dow30_table.find_elements_by_tag_name('tr')

        for item in dow30_items:
            name = item.find_element_by_class_name('wsod_firstCol').get_attribute('innerText').split('\xa0')[0]
            data = [txt.text for txt in item.find_elements_by_class_name("wsod_aRight")]
            DOW_composite_data[name] = data

        return DOW_composite_data

    def Close(self):
        self._client.quit()