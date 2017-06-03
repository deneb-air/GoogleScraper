# -*- coding: utf-8 -*-

import re
from urllib.parse import unquote

from SearchAnalyzer.parser.parser import Parser


class YahooParser(Parser):
    """Parses SERP pages of the Yahoo search engine."""

    search_engine = 'yahoo'

    search_types = ['normal', 'image']

    no_results_selector = []

    effective_query_selector = ['.msg #cquery a::attr(href)']

    num_results_search_selectors = ['#pg > span:last-child', '.compPagination span::text']

    page_number_selectors = ['#pg > strong::text']

    normal_search_selectors = {
        'results': {
            'de_ip': {
                'container': '#main',
                'result_container': '.res',
                'link': 'div > h3 > a::attr(href)',
                'snippet': 'div.abstr::text',
                'title': 'div > h3 > a::text',
                'visible_link': 'span.url::text'
            },
            'de_ip_december_2015': {
                'container': '#main',
                'result_container': '.searchCenterMiddle li',
                'link': 'h3.title a::attr(href)',
                'snippet': '.compText p::text',
                'title': 'h3.title a::text',
                'visible_link': 'span::text'
            },
        },
    }

    image_search_selectors = {
        'results': {
            'ch_ip': {
                'container': '#results',
                'result_container': '#sres > li',
                'link': 'a::attr(href)'
            },
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def after_parsing(self):
        """Clean the urls.

        The url is in the href attribute and the &imgurl= parameter.

        <a id="yui_3_5_1_1_1419284335995_1635" aria-label="<b>Matterhorn</b> sunrise"
        href="/images/view;_ylt=AwrB8phvj5hU7moAFzOJzbkF;_ylu=\
        X3oDMTIyc3ZrZ3RwBHNlYwNzcgRzbGsDaW1nBG9pZANmNTgyY2MyYTY4ZmVjYTI5YmYwNWZlM2E3ZTc1YzkyMARncG9zAzEEaXQDYmluZw--?
        .origin=&back=https%3A%2F%2Fimages.search.yahoo.com%2Fsearch%2Fimages%3F\
        p%3Dmatterhorn%26fr%3Dyfp-t-901%26fr2%3Dpiv-web%26tab%3Dorganic%26ri%3D1&w=4592&h=3056&
        imgurl=www.summitpost.org%2Fimages%2Foriginal%2F699696.JPG&rurl=http%3A%2F%2Fwww.summitpost.org\
        %2Fmatterhorn-sunrise%2F699696&size=5088.0KB&
        name=%3Cb%3EMatterhorn%3C%2Fb%3E+sunrise&p=matterhorn&oid=f582cc2a68feca29bf05fe3a7e75c920&fr2=piv-web&
        fr=yfp-t-901&tt=%3Cb%3EMatterhorn%3C%2Fb%3E+sunrise&b=0&ni=21&no=1&ts=&tab=organic&
        sigr=11j056ue0&sigb=134sbn4gc&sigi=11df3qlvm&sigt=10pd8j49h&sign=10pd8j49h&.crumb=qAIpMoHvtm1&\
        fr=yfp-t-901&fr2=piv-web">
        """
        super().after_parsing()

        if self.searchtype == 'normal':

            self.no_results = False
            if self.num_results == 0:
                self.no_results = True

            if len(self.dom.xpath(self.css_to_xpath('#cquery'))) >= 1:
                self.no_results = True

            for key, i in self.iter_serp_items():
                if self.search_results[key][i]['visible_link'] is None:
                    del self.search_results[key][i]

        if self.searchtype == 'image':
            for key, i in self.iter_serp_items():
                for regex in (
                        r'&imgurl=(?P<url>.*?)&',
                ):
                    result = re.search(regex, self.search_results[key][i]['link'])
                    if result:
                        # TODO: Fix this manual protocol adding by parsing "rurl"
                        self.search_results[key][i]['link'] = 'http://' + unquote(result.group('url'))
                        break
