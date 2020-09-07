"""
File:           url_parser.py
Author:         Dibyaranjan Sathua
Created on:     06/09/20, 4:36 PM

Code to except an URL and send http get request and return beautifulsoup object.
"""
from typing import Dict, Optional

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag


class URLParser:
    """ Parse URL and return the BeautifulSoup object """

    def __init__(self):
        self._session: requests.Session = requests.Session()
        self._default_header: Dict = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-IN,en;q=0.9,hi-IN;q=0.8,hi;q=0.7,en-GB;q=0.6,en-US;q=0.5",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
        }

    def parse(self, url: str, query_parameters: Optional[Dict[str, str]] = None,
              headers: Optional[Dict[str, str]] = None) -> Tag:
        """
        Parse URL
        Args:
            url: String
            query_parameters: dict, optional
            headers: dict, optional

        Returns: BeautifulSoup object
        """
        # Send get request to URL
        headers = headers if headers is not None else self._default_header
        page = self._session.get(url, data=query_parameters, headers=headers)
        # Raise exception for a 4XX client error or 5XX server error response
        page.raise_for_status()
        soup = BeautifulSoup(page.content, "html5lib")
        return soup

