"""
File:           console.py
Author:         Dibyaranjan Sathua
Created on:     07/09/20, 2:13 PM

Read inputs from console.
"""


class Console:
    """ Class to read console inputs """
    SellerName: str = ""
    TargetRating: int = 0
    MinProfit: float = 0
    FileName: str = ""

    @staticmethod
    def read():
        """ Read inputs from console """
        Console.SellerName = input("Enter your Amazon seller name: ")
        Console.TargetRating = int(input("Enter your target seller rating (___%): "))
        Console.FileName = input("Enter the file name for your product listings: ")
        Console.MinProfit = float(input("Enter your desired minimum profit: $"))
