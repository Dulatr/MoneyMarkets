from selenium import webdriver
from Tools import (
    isFailedResponse,
    getTableElements,
)

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

    def getTable(self,keystats: bool = False,markets: list = None) -> dict:
        """
        Get a table specified from the markets endpoint and whether to include keystats table. 
        """
        url = "https://money.cnn.com/data"

        response = {}
        DOW_composite_data ={}
        markets_data = {}

        if not(markets is None):
            try:
                for item in markets:
                    if not isinstance(item,str):
                        raise TypeError(f"'{item}' in argument 'markets' expected '{type(str)}', received '{type(item)}'.")
            except:
                if not isinstance(markets,str):
                    raise TypeError(f"'{markets}' in argument 'markets' expected '{type(str)}', received '{type(markets)}'.")

        if isinstance(markets,list):
            for item in markets:
                if isFailedResponse(url + f"/markets/{item}/"):
                    return {"Error":f"'{item}' in argument 'markets' not found."}
                
                # make a new dictionary
                response[item] = {}

                self._client.get(url + f"/markets/{item}/")

                try:
                    table_items = getTableElements(self._client,2)
                    for table_item in table_items:
                        row = table_item.get_attribute('innerText').split()
                        response[item][row[0]] = row[1:]
                except Exception as e:
                    pass
                    
                try:
                    self._client.find_element_by_id("fwd").click()
                    table_items = getTableElements(self._client,2)
                    for table_item in table_items:
                        row = thing.get_attribute('innerText').split()
                        response[item][row[0]] = row[1:]
                except Exception as e:
                    pass
        else:
            self._client.get(url + f"/markets/{markets}/")
            
            try:
                table_items = getTableElements(self._client,2)
                for table_item in table_items:
                    row = table_item.get_attribute('innerText').split()
                    response[item][row[0]] = row[1:]
            except Exception as e:
                print(e)

        if keystats:
            self._client.get(url + "/dow30/")
            dow30_items = getTableElements(self._client)

            for item in dow30_items:
                name = item.find_element_by_class_name('wsod_firstCol').get_attribute('innerText').split('\xa0')[0]
                data = [txt.text for txt in item.find_elements_by_class_name("wsod_aRight")]
                DOW_composite_data[name] = data

            response["keystats"] = DOW_composite_data
        
        return response
    
    def getUpdated(self):
        self._client.get("https://money.cnn.com/data/markets/")
        response = self._client.find_element_by_css_selector("div.disclaimer").get_attribute('innerText')
        return response

    def Close(self):
        self._client.quit()