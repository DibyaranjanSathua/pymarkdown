"""
File:           product.py
Author:         Dibyaranjan Sathua
Created on:     06/09/20, 5:01 PM

Code for Product class to store product information.
"""
from typing import List
import math


class Product:
    """ Product class stores the product information """
    AMAZON_FEE: float = 0.07
    MEDIA_BASE: float = 2.72
    MEDIA_RATE: float = 0.5
    FIRST_CLASS: List[float] = [2.04, 2.04, 2.04, 2.13, 2.22, 2.35, 2.53, 2.71]

    def __init__(self, name: str, asin: str, weight: float):
        self._name: str = name
        self._asin: str = asin
        # weight positive = pounds, negative = ounces
        self._weight: float = weight
        self._shipping_rate: float = self.calculate_shipping_rate(self._weight)

    @staticmethod
    def calculate_shipping_rate(weight: float) -> float:
        if weight >= 0:
            lbs: int = round(math.ceil(weight))      # Output of round is int type
            return Product.MEDIA_BASE + (lbs - 1) * Product.MEDIA_RATE + Product.AMAZON_FEE

        oz: int = round(math.ceil(-weight))
        if oz > len(Product.FIRST_CLASS):
            return Product.MEDIA_BASE + Product.AMAZON_FEE

        return Product.FIRST_CLASS[oz - 1] + Product.AMAZON_FEE

    # Python setters and getters
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def asin(self) -> str:
        return self._asin

    @asin.setter
    def asin(self, value: str) -> None:
        self._asin = value

    @property
    def weight(self) -> float:
        return self._weight

    @weight.setter
    def weight(self, value: float) -> None:
        self._weight = value
        self._shipping_rate = self.calculate_shipping_rate(self._weight)

    @property
    def shipping_rate(self) -> float:
        return self._shipping_rate

    def __repr__(self):
        return f"{self._name}: {self._asin}"

    def __str__(self):
        return self.__repr__()
