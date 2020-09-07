#! /usr/bin/env python3
"""
File:           main.py
Author:         Dibyaranjan Sathua
Created on:     07/09/20, 2:05 PM
"""
from src.console import Console
from src.amazon import Amazon


if __name__ == "__main__":
    Console.read()
    amazon = Amazon(
        seller_name=Console.SellerName,
        target_rating=Console.TargetRating,
        min_profit=Console.MinProfit,
        input_file=Console.FileName
    )
    amazon.run()
