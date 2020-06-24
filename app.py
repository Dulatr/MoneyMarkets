from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

import os
import time
from Tools import (
    isFailedResponse,
    getTableElements,
    isUp,
    buildDict
)

class App:
    def __init__(self,client: webdriver.Chrome,**kwargs):
        self._configuration = kwargs
        if not("startUrl" in kwargs.keys()):
            self._configuration["startUrl"] = "https://money.cnn.com/data/markets/"
        self._client = client
    
    def getStatus(self) -> str:
        if isUp(self._configuration["startUrl"]):
            return "OK"
        return "No connection"  

    def getUpdated(self):
        if self.getStatus() == "No connection":
            return ""
        self._client.get("https://money.cnn.com/data/markets/")
        response = self._client.find_element_by_css_selector("div.disclaimer").get_attribute('innerText')
        return response

class Stock(App):
    
    def getOverview(self):
        overview_data = {}
        self._client.get("https://money.cnn.com/data/markets/")
    
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
                        raise TypeError(f"'{item}' in argument 'markets' expected '{str}', received '{type(item)}'.")
            except:
                if not isinstance(markets,str):
                    raise TypeError(f"'{markets}' in argument 'markets' expected '{str}', received '{type(markets)}'.")

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
                        row = table_item.get_attribute('innerText').split()
                        response[item][row[0]] = row[1:]
                except Exception as e:
                    pass
        else:
            raise TypeError("Invalid type for argument 'markets'. Expected list.")
        
        if keystats:
            self._client.get(url + "/dow30/")
            dow30_items = getTableElements(self._client)

            for item in dow30_items:
                name = item.find_element_by_class_name('wsod_firstCol').get_attribute('innerText').split('\xa0')[0]
                data = [txt.text for txt in item.find_elements_by_class_name("wsod_aRight")]
                DOW_composite_data[name] = data

            response["keystats"] = DOW_composite_data
        
        return response

    def getHot(self) -> dict:
        self._client.get("https://money.cnn.com/data/hotstocks/index.html")
        actives = getTableElements(self._client,0)
        gainers = getTableElements(self._client,1)
        losers = getTableElements(self._client,2)

        keys = ["actives","gainers","losers"]
        active_data = {}
        gainer_data = {}
        losers_data = {}

        for (a,b,c) in zip(actives[1:],gainers[1:],losers[1:]):
            active_key = a.find_element_by_css_selector("a.wsod_symbol").get_attribute('innerText')
            gainer_key = b.find_element_by_css_selector("a.wsod_symbol").get_attribute('innerText')
            losers_key = c.find_element_by_css_selector("a.wsod_symbol").get_attribute('innerText')

            active_data[active_key] = []
            gainer_data[gainer_key] = []
            losers_data[losers_key] = []         

            active_tds = a.find_elements_by_css_selector("td.wsod_aRight")
            gainer_tds = b.find_elements_by_css_selector("td.wsod_aRight")
            losers_tds = c.find_elements_by_css_selector("td.wsod_aRight")

            for (td_a,td_b,td_c) in zip(active_tds,gainer_tds,losers_tds):
                active_data[active_key].append(td_a.get_attribute('innerText'))
                gainer_data[gainer_key].append(td_b.get_attribute('innerText'))
                losers_data[losers_key].append(td_c.get_attribute('innerText'))

        data = buildDict(keys,active_data,gainer_data,losers_data)
        return data

    def Close(self):
        self._client.quit()

class Story(App):

    def getPage(self,page: list = None,img: bool = False,save: bool = False,path: str = None) -> dict:
        """
        Get a news story information from a specific page.

        :Args:
            --page: page to pull stories from, currently only accepts ['front'].
            --img: boolean to determine whether to write out associated img info.
            --save: boolean to determine whether to save image data. only works with img=True.
            --path: path to save image data. defaults to <current program dir>/img/News/

        :Output:
            --dict: a dictionary object is returned with structure:
                    dict[page][story]{[title][web_link][path]}
        """
        if (path is None) and save:
            path = os.getcwd() + "/img/News/"

        if page is None:
            return {}
        if not(page[0] in ('front','investing')):
            return {"Error": f"""`{page}` not a viable page. Expected `('front','investing')`"""}
        
        self._client.get("https://money.cnn.com/data/markets/")
        data = {}
        for item in page:
            if item == 'front':
                news_list = self._client.find_elements_by_css_selector("li.summary")
                data[item] = {}
                story_num = 1
                for news_story in news_list:
                    data[item][f"story{story_num}"] = {}
                    data[item][f"story{story_num}"]["title"] = news_story.get_attribute('innerText')
                    data[item][f"story{story_num}"]["web_link"] = news_story.find_element_by_css_selector("a.summary-hed").get_attribute('href')
                    if img:
                        try:
                            src = news_story.find_element_by_tag_name("img").get_attribute('src')
                            data[item][f"story{story_num}"]["img_link"] = src
                        except:
                            data[item][f"story{story_num}"]["img_link"] = ''                        
                    story_num += 1
                if img and save:
                    img_num = 1
                    for story in data[item]:
                        try:
                            self._client.get(data[item][story]["img_link"])
                            _saved_to = f"{path}story{img_num}.png"
                            self._client.save_screenshot(_saved_to)
                            data[item][story]["path"] = _saved_to
                        except:
                            pass
                        img_num += 1
        return data

class Money(App):
    def __init__(self,client: webdriver.Chrome,**kwargs):
        self._configuration = kwargs
        if not("startUrl" in kwargs.keys()):
            self._configuration["startUrl"] = "https://money.cnn.com/data/world_markets/americas/"
        self._configuration["pairList"] = []
        self._client = client
        
        self._client.get(self._configuration["startUrl"])
        self._client.switch_to_frame(self._client.find_element_by_id("wsod_currencyConverterIframe"))   

        pairsBox = self._client.find_element_by_name("wsod_cc_baseCurrency")
        toBox = self._client.find_element_by_name("wsod_ccQuoteCurrency")
        self._configuration["boxList"] = [pairsBox,toBox]

        pairItems = pairsBox.find_elements_by_tag_name("option")
        for pairitem in pairItems:
            self._configuration["pairList"].append(pairitem.get_property("value"))

    def inputAmount(self,amount: float) -> None:
        inputBox = self._client.find_element_by_class_name("wsod_symSearchBox")
        inputBox.click()       
        inputBox.clear()
        inputBox.send_keys(str(amount))
        inputBox.send_keys(Keys.RETURN)
    
    def selectPair(self,_from: str,_to: str) -> None:
        if not(_from in self._configuration["pairList"]) or not(_to in self._configuration["pairList"]):
            raise ValueError(f"({_from},{_to}) not found in currency pair list: {self._configuration['pairList']}")
        choose = Select(self._configuration["boxList"][0])
        choose.select_by_value(_from)
        choose = Select(self._configuration["boxList"][1])
        choose.select_by_value(_to)

    def getConverted(self) -> str:
        time.sleep(0.75)
        return self._client.find_element_by_css_selector("div.wsod_ccResult").get_attribute("innerText").split()[1]