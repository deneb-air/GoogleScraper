# -*- coding: utf-8 -*-

import re

from SearchAnalyzer.parser.parser import Parser, logger


class YandexParser(Parser):
    """Parses SERP pages of the Yandex search engine."""

    search_engine = 'yandex'

    search_types = ['normal', 'image']

    no_results_selector = ['.message .misspell__message::text']

    effective_query_selector = ['.misspell__message .misspell__link']

    # @TODO: In december 2015, I saw that yandex only shows the number of search results in the search input field
    # with javascript. One can scrape it in plain http mode, but the values are hidden in some javascript and not
    # accessible with normal xpath/css selectors. A normal text search is done.
    num_results_search_selectors = [
        '.serp-adv .serp-item__wrap > strong',
        '.input__found_visibility_visible font font::text'
    ]

    page_number_selectors = ['.pager__group .button_checked_yes span::text']

    normal_search_selectors = {
        'results': {
            'de_ip': {
                'container': 'div.serp-list',
                'result_container': 'div.serp-item',
                'link': 'a.serp-item__title-link::attr(href)',
                'snippet': 'div.serp-item__text::text',
                'title': 'a.serp-item__title-link::text',
                'visible_link': 'a.serp-url__link::attr(href)'
            }
        }
    }

    image_search_selectors = {
        'results': {
            'de_ip': {
                'container': '.page-layout__content-wrapper',
                'result_container': '.serp-item__preview',
                'link': '.serp-item__preview .serp-item__link::attr(onmousedown)'
            },
            'de_ip_raw': {
                'container': '.page-layout__content-wrapper',
                'result_container': '.serp-item__preview',
                'link': '.serp-item__preview .serp-item__link::attr(href)'
            }
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def after_parsing(self):
        """Clean the urls.

        Normally Yandex image search store the image url in the onmousedown attribute in a json object. Its
        pretty messsy. This method grabs the link with a quick regex.

        c.hit({"dtype":"iweb","path":"8.228.471.241.184.141","pos":69,"reqid":\
        "1418919408668565-676535248248925882431999-ws35-986-IMG-p2"}, \
        {"href":"http://www.thewallpapers.org/wallpapers/3/382/thumb/600_winter-snow-nature002.jpg"});

        Sometimes the img url is also stored in the href attribute (when requesting with raw http packets).
        href="/images/search?text=snow&img_url=\
        http%3A%2F%2Fwww.proza.ru%2Fpics%2F2009%2F12%2F07%2F1290.jpg&pos=2&rpt=simage&pin=1">
        """
        super().after_parsing()

        if self.searchtype == 'normal':
            self.no_results = False

            if self.no_results_text:
                self.no_results = 'По вашему запросу ничего не нашлось' in self.no_results_text

            if self.num_results == 0:
                self.no_results = True

            # very hackish, probably prone to all kinds of errors.
            if not self.num_results_for_query:
                substr = 'function() { var title = "%s —' % self.query
                try:
                    i = self.html.index(substr)
                    if i:
                        self.num_results_for_query = re.search(
                            r'— (.)*?"',
                            self.html[i:i+len(self.query) + 150]
                        ).group()
                except Exception as e:
                    logger.debug(str(e))

        if self.searchtype == 'image':
            for key, i in self.iter_serp_items():
                for regex in (
                        r'\{"href"\s*:\s*"(?P<url>.*?)"\}',
                        r'img_url=(?P<url>.*?)&'
                ):
                    result = re.search(regex, self.search_results[key][i]['link'])
                    if result:
                        self.search_results[key][i]['link'] = result.group('url')
                        break
