"""
File:           repricer.py
Author:         Dibyaranjan Sathua
Created on:     07/09/20, 11:31 AM

Code for repricer.
"""
from typing import List, Optional
import sys

from src.product import Product
from src.product_listing import ProductListing
from src.condition import Condition


class Repricer:
    """ Class for repricer """
    VARIABLE_FEE_RATE = 0.15
    VARIABLE_CLOSING_FEE = 1.35
    PER_ITEM_FEE = 0.99
    EPSILON = 0.00001

    def __init__(self, product: Product, product_listings: List[ProductListing]):
        self._product: Product = product
        self._product_listings: List[ProductListing] = product_listings
        self._price_floor: float = 0.0
        self._price_ceiling: float = sys.float_info.max
        self._condition_filter: Condition = Condition.NONE
        self._rating_filter = 0

    def reprice(self, seller: Optional[ProductListing] = None) -> float:
        """ Reprice the seller price """
        if seller is None:
            seller = ProductListing()

        reprice_value = self._price_floor
        for listing in self._product_listings:
            total = listing.total
            if total > self._price_ceiling:
                break
            elif total < self._price_floor or listing.rating < self._rating_filter \
                    or listing.seller == seller.seller:
                continue

            if self._condition_filter == Condition.NEW:
                if listing.condition == Condition.NEW:
                    return listing.total - seller.shipping
            elif listing.condition.value >= self._condition_filter.value - 1:
                if abs(total - self._product_listings[0].total) < Repricer.EPSILON:
                    return listing.total - seller.shipping
                else:
                    return listing.total - seller.shipping - 0.01

            reprice_value = listing.total

        return reprice_value - seller.shipping

    def calculate_profit(self, price: float, shipping: float) -> float:
        """ Calculate profit """
        return price + shipping - Repricer.VARIABLE_FEE_RATE * price - \
               Repricer.VARIABLE_CLOSING_FEE - Repricer.PER_ITEM_FEE - self._product.shipping_rate

    # Getters and setters methods
    @property
    def product(self) -> Product:
        return self._product

    @product.setter
    def product(self, value: Product) -> None:
        self._product = value

    @property
    def product_listings(self) -> List[ProductListing]:
        return self._product_listings

    @product_listings.setter
    def product_listings(self, value: List[ProductListing]) -> None:
        self._product_listings = value

    @property
    def price_floor(self) -> float:
        return self._price_floor

    @price_floor.setter
    def price_floor(self, value: float) -> None:
        self._price_floor = value

    @property
    def price_ceiling(self) -> float:
        return self._price_ceiling

    @price_ceiling.setter
    def price_ceiling(self, value: float) -> None:
        self._price_ceiling = value

    @property
    def condition_filter(self) -> Condition:
        return self._condition_filter

    @condition_filter.setter
    def condition_filter(self, value: Condition) -> None:
        self._condition_filter = value

    @property
    def rating_filter(self) -> int:
        return self._rating_filter

    @rating_filter.setter
    def rating_filter(self, value: int) -> None:
        self._rating_filter = value