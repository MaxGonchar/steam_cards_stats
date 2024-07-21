import json
import re
from typing import List, Union, TypedDict
from functools import lru_cache
from datetime import datetime

from bs4 import BeautifulSoup

HystoryItem = List[Union[str, float]]


class ByAmount(TypedDict):
    price: str
    count: str


class Details(TypedDict):
    count: str
    prise: str
    details: ByAmount


class ParsedCardData(TypedDict):
    card_name: str
    game_name: str
    sale_details: Details
    buy_details: Details
    history: List[HystoryItem]


class CardParser:
    def __init__(self, html: str, appid: str):
        self.soup = BeautifulSoup(html, 'html.parser')
        self.appid = appid
        self.js_code = self.soup.find_all("script")[-1].text

    def parse(self) -> ParsedCardData:
        return {
            "card_name": self._get_card_name(),
            "game_name": self._get_game_name(),
            "sale_details": {
                "count": self._get_count_price("market_commodity_forsale")[0],
                "price": self._get_count_price("market_commodity_forsale")[1],
                "details": self._get_details("market_commodity_forsale_table"),
            },
            "buy_details": {
                "count": self._get_count_price("market_commodity_buyrequests")[0],
                "price": self._get_count_price("market_commodity_buyrequests")[1],
                "details": self._get_details("market_commodity_buyreqeusts_table"),
            },
            "history": self._get_history(),
            "date": datetime.utcnow().date(),
        }
    
    def _get_card_name(self) -> str:
        return self.soup.find("h1", {"id": "largeiteminfo_item_name"}).text
    
    def _get_game_name(self) -> str:
        start = "g_rgAppContextData = "
        finder = re.findall(rf'{start}.*;', self.js_code)
        dict_content = json.loads(finder[0][:-1].removeprefix(start))
        return dict_content[self.appid]["name"]

    @lru_cache(maxsize=None)
    def _get_count_price(self, element_id: str):
        return [el.text for el in self.soup.find("div", {"id": element_id}).findChildren("span")]
    
    def _get_details(self, element_id: str):
        rows = (
            self.soup.find("div", {"id": element_id})
            .find("table")
            .find("tbody")
            .find_all("tr")
        )
        res = []
        for row in rows:
            if data := row.find_all("td"):
                price, count = [i.text for i in data]
                res.append([price.split(" ")[0], count])

        return res
    
    def _get_history(self) -> List[HystoryItem]:
        start = "line1="
        finder = re.findall(rf'{start}.*;', self.js_code)
        history = json.loads(finder[0][:-1].removeprefix(start))
        return history
