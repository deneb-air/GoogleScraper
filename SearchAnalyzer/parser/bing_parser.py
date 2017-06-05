# -*- coding: utf-8 -*-

import re

from SearchAnalyzer.parser.parser import Parser


class BingParser(Parser):
    """Parses SERP pages of the Bing search engine."""

    search_engine = 'bing'

    search_types = ['normal', 'image']

    no_results_selector = ['#b_results > .b_no::text']

    num_results_search_selectors = ['.sb_count']

    effective_query_selector = ['#sp_requery a > strong', '#sp_requery + #sp_recourse a::attr(href)']

    page_number_selectors = ['.sb_pagS::text']

    total_results_re = re.compile('(\d+-\d+ )?([^0-9]*)(?P<total>[ ,.0-9]+)(.*)')

    normal_search_selectors = {
        'results': {
            'us_ip': {
                'container': '#b_results',
                'result_container': '.b_algo',
                'link': 'h2 > a::attr(href)',
                'snippet': '.b_caption > p::text',
                'title': 'h2::text',
                'visible_link': 'cite::text'
            },
            'de_ip': {
                'container': '#b_results',
                'result_container': '.b_algo',
                'link': 'h2 > a::attr(href)',
                'snippet': '.b_caption > p::text',
                'title': 'h2::text',
                'visible_link': 'cite::text'
            },
            'de_ip_news_items': {
                'container': 'ul.b_vList li',
                'link': ' h5 a::attr(href)',
                'snippet': 'p::text',
                'title': ' h5 a::text',
                'visible_link': 'cite::text'
            },
        },
        'ads_main': {
            'us_ip': {
                'container': '#b_results .b_ad',
                'result_container': '.sb_add',
                'link': 'h2 > a::attr(href)',
                'snippet': '.sb_addesc::text',
                'title': 'h2 > a::text',
                'visible_link': 'cite::text'
            },
            'de_ip': {
                'container': '#b_results .b_ad',
                'result_container': '.sb_add',
                'link': 'h2 > a::attr(href)',
                'snippet': '.b_caption > p::text',
                'title': 'h2 > a::text',
                'visible_link': 'cite::text'
            }
        }
    }

    image_search_selectors = {
        'results': {
            'ch_ip': {
                'container': '#dg_c .imgres',
                'result_container': '.dg_u',
                'link': 'a.dv_i::attr(m)'
            },
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def after_parsing(self):
        """Clean the urls.

        The image url data is in the m attribute.

        m={ns:"images.1_4",k:"5018",mid:"46CE8A1D71B04B408784F0219B488A5AE91F972E",
        surl:"http://berlin-germany.ca/",imgurl:"http://berlin-germany.ca/images/berlin250.jpg",
        oh:"184",tft:"45",oi:"http://berlin-germany.ca/images/berlin250.jpg"}
        """
        super().after_parsing()

        if self.searchtype == 'normal':

            self.no_results = False
            if self.no_results_text:
                self.no_results = self.query in self.no_results_text \
                    or 'Do you want results only for' in self.no_results_text

        if self.searchtype == 'image':
            for key, i in self.iter_serp_items():
                for regex in (
                        r'imgurl:"(?P<url>.*?)"',
                ):
                    result = re.search(regex, self.search_results[key][i]['link'])
                    if result:
                        self.search_results[key][i]['link'] = result.group('url')
                        break
