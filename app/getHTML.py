

import requests
from bs4 import BeautifulSoup

import time
import itertools

#検索画面へ　　→直下のレシピへ飛ぶ　→前材料を取得


class getDishInfo:

    def __init__(self,url):
        response = requests.get(url)
        self.htmls = BeautifulSoup(response.text,"html.parser")

    def stringTrim(self,string):
        setlist = string.split(")")
        return setlist[len(setlist)-1]
    

    
    def getProperQuantity(self):
        htmls = self.htmls
        quantity = htmls.find("section").find("h2").text.split("(")[1]
        if quantity[0].isdecimal():
            return int(quantity[0])
        else:
            return 2

    def getIngredients(self):
        htmls = self.htmls
        htmlss = htmls.find("section").find_all("ul")[1].find_all("li")
        quantity = self.getProperQuantity()
        setarray = []

        for ingredient in htmlss:
            setarray.append(ingredient.text.split())       
        for i in setarray:
            i[0] = self.stringTrim(i[0])
        
        return setarray

    def getDishName(self):
        htmls = self.htmls
        htmlss = htmls.find("section").find_all("ul")[0].find_all("li")
        array = htmlss[len(htmlss)-1].text.split()
        return "".join(array)



