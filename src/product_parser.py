"""
File:           product_parser.py
Author:         Dibyaranjan Sathua
Created on:     06/09/20, 5:25 PM

Code to parse product information from "http://www.amazon.com/gp/product/<asin_no>" page.
This class will use the URLParser class to parse the information using BeautifulSoup4.
"""
import re
from typing import Optional, List

from bs4.element import Tag

from src.url_parser import URLParser
from src.product import Product


class ProductParser:
    """ Parse the product information using BeautifulSoup4 """

    def __init__(self, url: str):
        self._url: str = url
        self._parser: URLParser = URLParser()
        self._soup: Optional[Tag] = None

    def parse(self) -> Product:
        """ Parse the URL and return Product object """
        self._soup = self._parser.parse(url=self._url)
        name: str = self._parse_name()
        asin: str = self._parse_asin()
        weight: float = self._parse_weight()
        return Product(name=name, asin=asin, weight=weight)

    def _parse_name(self) -> str:
        """ Parse the name """
        return self._soup.find("span", attrs={"id": "productTitle"}).text.strip()

    def _parse_product_details(self) -> List[str]:
        """ Parse the product details and return a list of details """
        details_div = self._soup.find("div", attrs={"id": "detailBullets_feature_div"})
        return [detail.text.strip().replace("\n", "") for detail in details_div.find_all("li")]

    def _parse_weight(self) -> float:
        """ Parse weight from the product details """
        weight_regex = re.compile(r":(\d+(?:\.\d+)?)\s+(\S+)")
        product_details = self._parse_product_details()
        for detail in product_details:
            if "weight" in detail.lower():
                match_obj = weight_regex.search(detail)
                # Return positive weight for pound and negative weight for ounces
                if match_obj is not None:
                    return float(match_obj.group(1)) \
                        if "pound" in match_obj.group(2).lower() \
                        else -float(match_obj.group(1))
        return 0.0

    def _parse_asin(self) -> str:
        """ Parse ASIN or ISBN-10 number from the product details """
        asin_regex = re.compile(r":(\d+)")
        product_details = self._parse_product_details()
        for detail in product_details:
            if "isbn-10" in detail.lower():
                match_obj = asin_regex.search(detail)
                if match_obj is not None:
                    return match_obj.group(1)
        return self._url.split("/")[-1]

    # Class getters and setters
    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, value: str) -> None:
        self._url = value


if __name__ == "__main__":
    test_url = "https://www.amazon.com/gp/product/0802136680"
    obj = ProductParser(test_url).parse()
    print(f"Name: {obj.name}")
    print(f"ASIN: {obj.asin}")
    print(f"Weight: {obj.weight}")
