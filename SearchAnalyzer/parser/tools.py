# -*- coding: utf-8 -*-

import os
import re
import sys

from SearchAnalyzer.database import SearchEngineResultsPage
from SearchAnalyzer.parser.ask_parser import AskParser
from SearchAnalyzer.parser.baidu_parser import BaiduParser
from SearchAnalyzer.parser.bing_parser import BingParser
from SearchAnalyzer.parser.blekko_parser import BlekkoParser
from SearchAnalyzer.parser.duckduckgo_parser import DuckduckgoParser
from SearchAnalyzer.parser.google_parser import GoogleParser
from SearchAnalyzer.parser.yahoo_parser import YahooParser
from SearchAnalyzer.parser.yandex_parser import YandexParser
from SearchAnalyzer.parser.exception import UnknowUrlException, NoParserForSearchEngineException


def get_parser_by_url(url):
    """Get the appropriate parser by an search engine url.

    Args:
        url: The url that was used to issue the search

    Returns:
        The correct parser that can parse results for this url.

    Raises:
        UnknowUrlException if no parser could be found for the url.
    """
    parser = None

    if re.search(r'^http[s]?://www\.google', url):
        parser = GoogleParser
    elif re.search(r'^http://yandex\.ru', url):
        parser = YandexParser
    elif re.search(r'^http://www\.bing\.', url):
        parser = BingParser
    elif re.search(r'^http[s]?://search\.yahoo.', url):
        parser = YahooParser
    elif re.search(r'^http://www\.baidu\.com', url):
        parser = BaiduParser
    elif re.search(r'^https://duckduckgo\.com', url):
        parser = DuckduckgoParser
    if re.search(r'^http[s]?://[a-z]{2}?\.ask', url):
        parser = AskParser
    if re.search(r'^http[s]?://blekko', url):
        parser = BlekkoParser
    if not parser:
        raise UnknowUrlException('No parser for {}.'.format(url))

    return parser


def get_parser_by_search_engine(search_engine):
    """Get the appropriate parser for the search_engine

    Args:
        search_engine: The name of a search_engine.

    Returns:
        A parser for the search_engine

    Raises:
        NoParserForSearchEngineException if no parser could be found for the name.
    """
    if search_engine == 'google' or search_engine == 'googleimg':
        return GoogleParser
    elif search_engine == 'yandex':
        return YandexParser
    elif search_engine == 'bing':
        return BingParser
    elif search_engine == 'yahoo':
        return YahooParser
    elif search_engine == 'baidu' or search_engine == 'baiduimg':
        return BaiduParser
    elif search_engine == 'duckduckgo':
        return DuckduckgoParser
    elif search_engine == 'ask':
        return AskParser
    elif search_engine == 'blekko':
        return BlekkoParser
    else:
        raise NoParserForSearchEngineException('No such parser for "{}"'.format(search_engine))


def parse_serp(config, html=None, parser=None, scraper=None, search_engine=None, query=''):
    """Store the parsed data in the sqlalchemy session.

    If no parser is supplied then we are expected to parse again with
    the provided html.

    This function may be called from scraping and caching.
    When called from caching, some info is lost (like current page number).

    Args:
        TODO: A whole lot

    Returns:
        The parsed SERP object.
    """

    if not parser and html:
        parser = get_parser_by_search_engine(search_engine)
        parser = parser(config, query=query)
        parser.parse(html)

    serp = SearchEngineResultsPage()

    if query:
        serp.query = query

    if parser:
        serp.set_values_from_parser(parser)
    if scraper:
        serp.set_values_from_scraper(scraper)

    return serp


if __name__ == '__main__':
    """Originally part of https://github.com/NikolaiT/SearchAnalyzer.
    
    Only for testing purposes: May be called directly with an search engine 
    search url. For example:
    
    python3 parsing.py 'http://yandex.ru/yandsearch?text=GoogleScraper&lr=178&csg=82%2C4317%2C20%2C20%2C0%2C0%2C0'
    
    Please note: Using this module directly makes little sense, because requesting such urls
    directly without imitating a real browser (which is done in my SearchAnalyzer module) makes
    the search engines return crippled html, which makes it impossible to parse.
    But for some engines it nevertheless works (for example: yandex, google, ...).
    """
    import requests

    assert len(sys.argv) >= 2, 'Usage: {} url/file'.format(sys.argv[0])
    url = sys.argv[1]
    if os.path.exists(url):
        raw_html = open(url, 'r').read()
        parser = get_parser_by_search_engine(sys.argv[2])
    else:
        raw_html = requests.get(url).text
        parser = get_parser_by_url(url)

    parser = parser(raw_html)
    parser.parse()
    print(parser)

    with open('/tmp/testhtml.html', 'w') as of:
        of.write(raw_html)
