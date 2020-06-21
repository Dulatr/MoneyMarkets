"""
A module for webdriver interactions.
"""
from selenium import webdriver
import requests

import sys

def isUp(url: str) -> bool:
    """
    Check url for status code 200
    """
    try:
        response = requests.get(url)
        return response.status_code == 200
    except:
        return False

def isFailedResponse(url: str) -> bool:
    """
    Check url for response code 404: page not found.
    """
    try:
        return requests.get(url).status_code == 404
    except:
        return True

def getTableElements(driver: webdriver.Chrome,tableIndex: int = 0) -> [webdriver.WebKitGTK._web_element_cls,...]:
    """
    Find a table with chrome webdriver.

    Returns a list of table row elements.
    """
    try:
        selector = driver.find_elements_by_css_selector("table.wsod_dataTableBig")
        table = selector[tableIndex].find_element_by_tag_name('tbody')
    except IndexError as i:
        selector = driver.find_elements_by_css_selector("table.wsod_dataTableBigAlt")
        table = selector[tableIndex].find_element_by_tag_name('tbody')
    except Exception as e:
        sys.stdout.write(e.args)
        return None
    
    return table.find_elements_by_tag_name('tr')

def buildDict(keys: list,*lists: list) -> dict:
    """
    From a set of desired keys, attach a list of data at that key.
    """
    if len(lists) != len(keys):
        raise ValueError("Number of keys must match the number of data lists.")

    dictionary = {}
    for key,_list in zip(keys,lists):
        dictionary[key] = _list
    return dictionary