# -*- coding: utf-8 -*-

"""
I switched my motto; instead of saying "fuck tomorrow"
That buck that bought a bottle could've struck the lotto.
"""

__author__ = 'Nikolai Tschacher'
__updated__ = '30.11.2015'  # day.month.year
__home__ = 'incolumitas.com'

from SearchAnalyzer.proxies import Proxy
from SearchAnalyzer.config import get_config
import logging

"""
All objects imported here are exposed as the public API of SearchAnalyzer
"""

from SearchAnalyzer.core import scrape_with_config
from SearchAnalyzer.scraping import GoogleSearchError, MaliciousRequestDetected

logging.getLogger(__name__)
