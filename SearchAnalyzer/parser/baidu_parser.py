# -*- coding: utf-8 -*-

import re
from urllib.parse import unquote

from SearchAnalyzer.parser.parser import Parser


class BaiduParser(Parser):
    """Parses SERP pages of the Baidu search engine."""

    search_engine = 'baidu'

    search_types = ['normal', 'image']

    num_results_search_selectors = ['#container .nums']

    no_results_selector = ['.content_none .nors p::text']

    # no such thing for baidu
    effective_query_selector = ['']

    page_number_selectors = ['.fk_cur + .pc::text']

    normal_search_selectors = {
        'results': {
            '2017-06-05': {
                'container': '#content_left',
                'result_container': '.result',
                'link': 'h3 > a::attr(href)',
                'snippet': '.c-abstract::text',
                'title': 'h3 > a::text',
                'visible_link': 'a.c-showurl::text'
            }
        }
    }

    image_search_selectors = {
        'results': {
            'ch_ip': {
                'container': '#imgContainer',
                'result_container': '.pageCon > li',
                'link': '.imgShow a::attr(href)'
            },
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def after_parsing(self):
        """Clean the urls.

        href="/i?ct=503316480&z=&tn=baiduimagedetail&ipn=d&word=matterhorn&step_word=&ie=utf-8&in=9250&
        cl=2&lm=-1&st=&cs=3326243323,1574167845&os=1495729451,4260959385&pn=0&rn=1&di=69455168860&ln=1285&
        fr=&&fmq=1419285032955_R&ic=&s=&se=&sme=0&tab=&width=&height=&face=&is=&istype=&ist=&jit=&
        objurl=http%3A%2F%2Fa669.phobos.apple.com%2Fus%2Fr1000%2F077%2FPurple%2F\
        v4%2F2a%2Fc6%2F15%2F2ac6156c-e23e-62fd-86ee-7a25c29a6c72%2Fmzl.otpvmwuj.1024x1024-65.jpg&adpicid=0"
        """
        super().after_parsing()

        if self.searchtype == 'normal':
            self.no_results = False
            if self.no_results_text:
                self.no_results = True

        if self.searchtype == 'image':
            for key, i in self.iter_serp_items():
                for regex in (
                        r'&objurl=(?P<url>.*?)&',
                ):
                    result = re.search(regex, self.search_results[key][i]['link'])
                    if result:
                        self.search_results[key][i]['link'] = unquote(result.group('url'))
                        break
