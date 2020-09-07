"""
File:           product_listing.py
Author:         Dibyaranjan Sathua
Created on:     06/09/20, 7:11 PM

Stores the product listing information from "http://www.amazon.com/gp/offer-listing/" site.
"""
from typing import Optional

from src.condition import Condition
from src.console import Console


class ProductListing:
    """ Product Listing class """
    DEFAULT_SHIPPING: float = 3.99
    DEFAULT_TAX: float = 0.0

    def __init__(self, seller: Optional[str] = None, price: float = 0.0, rating: int = 0,
                 total_ratings: int = 0, condition: Condition = Condition.NONE,
                 tax: float = DEFAULT_TAX, shipping: float = DEFAULT_SHIPPING):
        self._seller: str = seller
        self._price: float = price
        self._shipping: float = shipping
        self._tax: float = tax
        self._rating: int = rating
        self._total_ratings: int = total_ratings
        self._condition: Condition = condition

        if self._seller is None:
            self._seller = Console.SellerName

        self._total = self._get_total()

    def _get_total(self):
        return self._price + self._shipping + self._tax

    # Class getters and setters
    @property
    def seller(self) -> str:
        return self._seller

    @seller.setter
    def seller(self, value: str) -> None:
        self._seller = value

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        self._price = value
        self._total = self._get_total()

    @property
    def shipping(self) -> float:
        return self._shipping

    @shipping.setter
    def shipping(self, value: float) -> None:
        self._shipping = value
        self._total = self._get_total()

    @property
    def tax(self) -> float:
        return self._tax

    @tax.setter
    def tax(self, value: float) -> None:
        self._tax = value
        self._total = self._get_total()

    @property
    def rating(self) -> int:
        return self._rating

    @rating.setter
    def rating(self, value: int) -> None:
        self._rating = value

    @property
    def total_ratings(self) -> int:
        return self._total_ratings

    @total_ratings.setter
    def total_ratings(self, value: int) -> None:
        self._total_ratings = value

    @property
    def condition(self) -> Condition:
        return self._condition

    @condition.setter
    def condition(self, value: Condition) -> None:
        self._condition = value

    @property
    def total(self) -> float:
        return self._total

    def __repr__(self):
        return f"{self._seller}: ${self._price:.2f} + ${self._shipping:.2f} shipping"

    def __str__(self):
        self.__repr__()

    def __eq__(self, other):
        return self.total == other.total and self.condition == other.condition and \
               self.rating == other.rating and self.total_ratings == other.total_ratings

    def __lt__(self, other):
        if self.total == other.total:
            if self.condition == other.condition:
                if self.rating == other.rating:
                    return self.total_ratings > other.total_ratings
                return self.rating > other.rating
            return self.condition > other.condition
        return self.total < other.total

    def __gt__(self, other):
        if self.total == other.total:
            if self.condition == other.condition:
                if self.rating == other.rating:
                    return self.total_ratings < other.total_ratings
                return self.rating < other.rating
            return self.condition < other.condition
        return self.total > other.total
