"""
File:           amazon.py
Author:         Dibyaranjan Sathua
Created on:     07/09/20, 11:46 AM
"""
from typing import List
import os

from src.product import Product
from src.product_parser import ProductParser
from src.product_listing import ProductListing
from src.product_listing_parser import ProductListingParser
from src.repricer import Repricer
from src.condition import Condition


class Amazon:
    """ Class for Amazon """
    PRODUCT_URL: str = "http://www.amazon.com/gp/product/{}"
    LISTING_URL: str = "http://www.amazon.com/gp/offer-listing/{}/ref=olp_tab_all"

    def __init__(self, seller_name: str, target_rating: float, min_profit: float, input_file: str):
        self._seller_name = seller_name
        self._target_rating = target_rating
        self._min_profit = min_profit
        self._input_file = os.path.abspath(input_file)
        self._unprofitable: List[str] = []

    def process_input(self):
        """ Read the product information from the file """
        output_file = self._get_output_file(self._input_file)
        with open(output_file, mode="w") as output_file:
            with open(self._input_file, mode="r") as infile:
                for line in infile:
                    line = line.strip()
                    line_values = line.split()
                    asin: str = line_values[0]
                    condition: int = int(line_values[1])

                    print(f"Processing ASIN: {asin}")

                    product_url = Amazon.PRODUCT_URL.format(asin)
                    product_listing_url = Amazon.LISTING_URL.format(asin)

                    print(f"Parsing product")
                    product: Product = ProductParser(product_url).parse()
                    product_listing_parser: ProductListingParser = \
                        ProductListingParser(product_listing_url)
                    print(f"Parsing product listings")
                    product_listings: List[ProductListing] = product_listing_parser.parse()

                    print(f"Repricing")
                    repricer: Repricer = Repricer(product, product_listings)
                    my_product_listing: ProductListing = product_listing_parser.my_listing
                    repricer.rating_filter = self._target_rating
                    repricer.condition_filter = Condition(condition)

                    price = repricer.reprice(my_product_listing)
                    profit = repricer.calculate_profit(price, my_product_listing.shipping)

                    print(f"Mew Price: {price:.2f}")
                    print(f"Profit: {profit:.2f}")

                    # Output to file
                    if profit > self._min_profit:
                        output_file.write(f"{product}\n")
                        output_file.write(f"{price:.2f}\n\n")
                    else:
                        self._unprofitable.append(str(product))

                    print(f"Completed!!!\n\n")

    def run(self):
        """ Entry function """
        self.process_input()

        if self._unprofitable:
            print(f"These products did not meet the ${self._min_profit:.2f} minimum profit")
            for element in self._unprofitable:
                print(element)

    @staticmethod
    def _get_output_file(filename):
        """ Return the output file path from input file path """
        name, ext = os.path.splitext(os.path.abspath(filename))
        output_name = f"{name}_output"
        return f"{output_name}{ext}"

