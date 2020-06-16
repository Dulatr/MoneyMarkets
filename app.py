from selenium import webdriver
import os
from Tools import (
    isFailedResponse,
    getTableElements,
)


class Stock:

    def __init__(self,client: webdriver.Chrome,**kwargs):
        self._configuration = kwargs
        self._client = client
    
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
                        row = thing.get_attribute('innerText').split()
                        response[item][row[0]] = row[1:]
                except Exception as e:
                    pass
        elif isinstance(markets,str):
            self._client.get(url + f"/markets/{markets}/")

            try:
                table_items = getTableElements(self._client,2)
                for table_item in table_items:
                    row = table_item.get_attribute('innerText').split()
                    response[item][row[0]] = row[1:]
            except Exception as e:
                pass
 
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

class Story:
    
    def __init__(self,client: webdriver.Chrome,**kwargs):
        self._configuration = kwargs
        self._client = client

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
                            _saved_to = f"{path}story_image{img_num}.png"
                            self._client.save_screenshot(_saved_to)
                            data[item][story]["path"] = _saved_to
                        except:
                            pass
                        img_num += 1
        return data
    
    def getUpdated(self):
        self._client.get("https://money.cnn.com/data/markets/")
        response = self._client.find_element_by_css_selector("div.disclaimer").get_attribute('innerText')
        return response
