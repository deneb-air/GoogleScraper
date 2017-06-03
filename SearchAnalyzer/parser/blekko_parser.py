# -*- coding: utf-8 -*-

from SearchAnalyzer.parser.parser import Parser


class BlekkoParser(Parser):
    """Parses SERP pages of the Blekko search engine."""

    search_engine = 'blekko'

    search_types = ['normal']

    effective_query_selector = ['']

    no_results_selector = []

    num_results_search_selectors = []

    normal_search_selectors = {
        'results': {
            'de_ip': {
                'container': '#links',
                'result_container': '.result',
                'link': '.result__title > a::attr(href)',
                'snippet': 'result__snippet::text',
                'title': '.result__title > a::text',
                'visible_link': '.result__url__domain::text'
            }
        },
    }
