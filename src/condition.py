"""
File:           condition.py
Author:         Dibyaranjan Sathua
Created on:     06/09/20, 10:26 PM
"""
import enum


class Condition(enum.IntEnum):
    """ Condition constants """
    NEW = 9
    USED_LIKE_NEW = 8
    USED_VERY_GOOD = 7
    USED_GOOD = 6
    USED_ACCEPTABLE = 5
    COLLECTIBLE_LIKE_NEW = 4
    COLLECTIBLE_VERY_GOOD = 3
    COLLECTIBLE_GOOD = 2
    COLLECTIBLE_ACCEPTABLE = 1
    NONE = 0        # This represent None of the above condition
