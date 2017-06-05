# -*- coding: utf-8 -*-

import re
from urllib.parse import unquote

from SearchAnalyzer.parser.google_parser import GoogleParser


class GoogleUAParser(GoogleParser):
    """Parses SERP pages of the Google search engine."""

    search_engine = 'google_ua'

    total_results_re = re.compile('(Сторінка \d+ )?([^0-9]*)(?P<total>[\xa0 ,.0-9]+)(.*)')
