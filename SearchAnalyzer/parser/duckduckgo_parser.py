# -*- coding: utf-8 -*-

from SearchAnalyzer.parser.parser import Parser


class DuckduckgoParser(Parser):
    """Parses SERP pages of the Duckduckgo search engine."""

    search_engine = 'duckduckgo'

    search_types = ['normal']

    num_results_search_selectors = []

    no_results_selector = []

    effective_query_selector = ['']

    # duckduckgo is loads next pages with ajax
    page_number_selectors = ['']

    normal_search_selectors = {
        'results': {
            'de_ip': {
                'container': '#links',
                'result_container': '.result',
                'link': '.result__title > a::attr(href)',
                'snippet': 'result__snippet::text',
                'title': '.result__title > a::text',
                'visible_link': '.result__url__domain::text'
            },
            'non_javascript_mode': {
                'container': '#content',
                'result_container': '.results_links',
                'link': '.links_main > a::attr(href)',
                'snippet': '.snippet::text',
                'title': '.links_main > a::text',
                'visible_link': '.url::text'
            },
        },
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def after_parsing(self):
        super().after_parsing()

        if self.searchtype == 'normal':

            try:
                if 'No more results.' in self.dom.xpath(self.css_to_xpath('.no-results'))[0].text_content():
                    self.no_results = True
            except:
                pass

            if self.num_results > 0:
                self.no_results = False
            elif self.num_results <= 0:
                self.no_results = True
