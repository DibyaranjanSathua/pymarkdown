"""
File:           product_listing_parser.py
Author:         Dibyaranjan Sathua
Created on:     06/09/20, 10:20 PM

Code to parse product listing information from "http://www.amazon.com/gp/offer-listing/".
"""
from typing import List, Optional
import re
from urllib.parse import urljoin
import time

from bs4.element import Tag

from src.product_listing import ProductListing
from src.url_parser import URLParser
from src.condition import Condition
from src.console import Console


class ProductListingParser:
    """ Parse product listing information using BeautifulSoup4 """
    BASE_URL = "https://www.amazon.com/"

    def __init__(self, url: str):
        self._url: str = url
        self._product_listings: List[ProductListing] = []
        self._parser: URLParser = URLParser()
        self._soup: Optional[Tag] = None

    def parse(self) -> List[ProductListing]:
        """ Parse the product listing page """
        url_to_parse = self._url
        while True:
            self._soup: Tag = self._parser.parse(url=url_to_parse)
            listings: List[Tag] = self._soup.find_all(
                "div",
                attrs={"class": "a-row a-spacing-mini olpOffer"}
            )
            for row in listings:
                price: float = self._parse_price(row)
                seller: str = self._parse_seller(row)
                rating: int = self._parse_rating(row)
                no_of_ratings: int = self._parse_no_of_ratings(row)
                condition: Condition = Condition(self._parse_condition(row))
                self._product_listings.append(
                    ProductListing(
                        seller=seller,
                        price=price,
                        rating=rating,
                        total_ratings=no_of_ratings,
                        condition=condition
                    )
                )

            url_to_parse = self._parse_next_link(self._soup)
            if url_to_parse is None:
                break

            # Wait for 1 sec before scrapping next page
            time.sleep(1)

        return self._product_listings

    @staticmethod
    def _parse_price(row_listing: Tag) -> float:
        """ Parse the price from a row of listing """
        price = row_listing.find("div", attrs={"class": "olpPriceColumn"}).text.strip().\
            replace("\n", "")
        price_regex = re.compile(r"(\d+(?:\.\d+)?)")
        match_obj = price_regex.search(price)
        return float(match_obj.group(1)) if match_obj is not None else 0.0

    @staticmethod
    def _parse_shipping(row_listing: Tag) -> float:
        """ Parse the shipping value from a row of listing """
        shipping = row_listing.find("div", attrs={"class": "olpPriceColumn"}).\
            find("p", attrs={"class": "olpShippingInfo"})
        return float(shipping.text.strip().replace("\n", "")) if shipping is not None else 0.0

    @staticmethod
    def _parse_tax(row_listing: Tag) -> float:
        """ Parse tax information from a row of listing """
        pass

    @staticmethod
    def _parse_seller(row_listing: Tag) -> str:
        """ Parse the seller from a row of listing """
        seller = row_listing.find("div", attrs={"class": "olpSellerColumn"})
        seller = seller.find("h3", attrs={"class": "olpSellerName"})
        return seller.text.strip().replace("\n", "") if seller is not None else "Amazon.com"

    @staticmethod
    def _parse_rating(row_listing: Tag) -> int:
        """ Parse rating from a row of listing """
        details = row_listing.find("div", attrs={"class": "olpSellerColumn"})
        rating = details.find("p")
        if rating is None:
            return 100
        rating = rating.text.strip().replace("\n", "")
        rating_regex = re.compile(r"(\d+)\s*%")
        match_obj = rating_regex.search(rating)
        return int(match_obj.group(1)) if match_obj is not None else 100

    @staticmethod
    def _parse_no_of_ratings(row_listing: Tag) -> int:
        """ Parse no of user ratings from a row of listing """
        details = row_listing.find("div", attrs={"class": "olpSellerColumn"})
        no_of_ratings = details.find("p")
        if no_of_ratings is None:
            return 0
        no_of_ratings = no_of_ratings.text.strip().replace("\n", "")
        no_of_ratings_regex = re.compile(r"\(\s*(\d+).*\)")
        match_obj = no_of_ratings_regex.search(no_of_ratings)
        return int(match_obj.group(1)) if match_obj is not None else 0

    @staticmethod
    def _parse_condition(row_listing: Tag) -> int:
        """ Parse the condition from a row of listing """
        condition_mapping = {
            "New": Condition.NEW,
            "Used-LikeNew": Condition.USED_LIKE_NEW,
            "Used-VeryGood": Condition.USED_VERY_GOOD,
            "Used-Good": Condition.USED_GOOD,
            "Used-Acceptable": Condition.USED_ACCEPTABLE,
            "Collectible-LikeNew": Condition.COLLECTIBLE_LIKE_NEW,
            "Collectible-VeryGood": Condition.COLLECTIBLE_VERY_GOOD,
            "Collectible-Good": Condition.COLLECTIBLE_GOOD,
            "Collectible-Acceptable": Condition.COLLECTIBLE_ACCEPTABLE
        }
        # Removing all the spaces to normalize the string for easier comparison
        condition = row_listing.find("div", attrs={"class": "olpConditionColumn"}).\
            find("span", attrs={"class": "olpCondition"}).text.strip().\
            replace("\n", "").replace(" ", "")
        return condition_mapping[condition].value

    @staticmethod
    def _parse_next_link(html_page: Tag) -> Optional[str]:
        pagination = html_page.find("ul", attrs={"class": "a-pagination"})
        # pagination will not be present in the listings are less than 10
        if pagination is None:
            return None
        next_link = pagination.find("li", attrs={"class": "a-last"})
        if next_link is None:
            return None
        next_link = next_link.find("a")
        if next_link is None:
            return None
        # next link is None means we are in the last page
        return urljoin(ProductListingParser.BASE_URL, next_link.attrs["href"])

    # Class getters and setters
    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, value: str) -> None:
        self._url = value

    @property
    def product_listings(self) -> List[ProductListing]:
        return self._product_listings

    @property
    def my_listing(self) -> ProductListing:
        for listing in self._product_listings:
            if listing.seller == Console.SellerName:
                return listing
        return ProductListing()


if __name__ == "__main__":
    test_url = "https://www.amazon.com/gp/offer-listing/0802136680/ref=olp_tab_all"
    test_listings = ProductListingParser(test_url).parse()
    for row in test_listings:
        print(f"Seller: {row.seller}, Price: {row.price}, Rating: {row.rating}, "
              f"Total_ratings: {row.total_ratings}, Condition: {row.condition}, "
              f"Shipping: {row.shipping}, Tax: {row.tax}")

