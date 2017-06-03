# -*- coding: utf-8 -*-

from SearchAnalyzer.parser.parser import Parser


class AskParser(Parser):
    """Parses SERP pages of the Ask search engine."""

    search_engine = 'ask'

    search_types = ['normal']

    num_results_search_selectors = []

    no_results_selector = []

    effective_query_selector = ['#spell-check-result > a']

    page_number_selectors = ['.pgcsel .pg::text']

    normal_search_selectors = {
        'results': {
            'de_ip': {
                'container': '#midblock',
                'result_container': '.ptbs.ur',
                'link': '.abstract > a::attr(href)',
                'snippet': '.abstract::text',
                'title': '.txt_lg.b::text',
                'visible_link': '.durl span::text'
            }
        },
    }
