# -*- coding: utf-8 -*-

import os
import unittest
from collections import namedtuple

# from SearchAnalyzer import scrape_with_config
from SearchAnalyzer.config import get_config
from SearchAnalyzer.parser.tools import get_parser_by_search_engine

Expect = namedtuple('Expect', [
    'no_results',
    'results_for_query',
    'total_results',
    'num_results',
    'page_number',
    'num_links',
    'visible_link',
    'snippet'
])


class ParserTestCase(unittest.TestCase):
    config = get_config()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # Test (very) static parsing for all search engines. The html files are saved in 'data/uncompressed_serp_pages/'
    # The sample files may become old and the SERP format may change over time. But this is the only
    # way to assert that a certain url or piece must be in the results.
    # If the SERP format changes, update accordingly (after all, this shouldn't happen that often).
    @staticmethod
    def get_parser_for_file(se, file, **kwargs):
        base = os.path.dirname(os.path.realpath(__file__))
        file = os.path.join(base, file)
        with open(file, 'r') as f:
            html = f.read()
            parser = get_parser_by_search_engine(se)
            parser = parser(ParserTestCase.config, html, **kwargs)

        return parser

    # test normal search result page
    def _test_engine_normal(self, se, filename, expect):
        parser = self.get_parser_for_file(se, filename)

        self.assertFalse(parser.no_results)

        self.assertIn(expect.results_for_query, parser.num_results_for_query)
        self.assertEqual(expect.total_results, parser.total_results)
        self.assertEqual(expect.num_results, parser.num_results)

        self.assertEqual(expect.page_number, parser.page_number)

        self.assertEqual(expect.num_links, len(parser.search_results['results']))
        self.assertTrue(all(res['link'] for res in parser.search_results['results']))
        self.assertTrue(all(res['visible_link'] for res in parser.search_results['results']))

        self.assertTrue(
            any([
                expect.visible_link in res['visible_link']
                for res in parser.search_results['results']
            ]),
            'There is not a link \'{}\' in results'.format(expect.visible_link)
        )
        self.assertTrue(
            any([
                expect.snippet in res['snippet'] if res['snippet'] else False
                for res in parser.search_results['results']
            ]),
            'There is not result with \'{}\' snippet'.format(expect.snippet)
        )

    # test 'not found' page
    def _test_engine_not_found(self, se, filename):
        parser = self.get_parser_for_file(se, filename)

        self.assertTrue(parser.no_results)
        # self.assertFalse(parser.num_results_for_query)
        self.assertEqual(0, parser.total_results)
        self.assertEqual(0, parser.num_results)
        self.assertEqual(0, parser.page_number)
        self.assertListEqual([], parser.search_results['results'])

    # google
    def test_google(self):
        self._test_engine_normal('google', 'data/uncompressed_2017/google_670120.1_p1.html', Expect(
            False,                               # no_results
            'About 540 results (0.26 seconds)',  # results_for_query
            540,                                 # total_results
            9,                                   # num_results
            1,                                   # page_number
            9,                                   # num_links
            'agrodoctor.ua',                     # visible_link
            'Knife Head 670120.1+676231.0'       # snippet
        ))

        self._test_engine_normal('google', 'data/uncompressed_2017/google_samsung_p7.html', Expect(
            False,                                                   # no_results
            'Page 7 of about 1,470,000,000 results (0.77 seconds)',  # results_for_query
            1470000000,                                              # total_results
            13,                                                      # num_results
            7,                                                       # page_number
            10,                                                      # num_links
            'thinktankteam.info',                                    # visible_link
            'Oculus mobile platform transforms'                      # snippet
        ))

        self._test_engine_not_found('google', 'data/uncompressed_2017/google_not_found.html')

    # bing
    def test_bing(self):
        self._test_engine_normal('bing', 'data/uncompressed_2017/bing_670120.1_p1.html', Expect(
            False,  # no_results
            '1,430 results',  # results_for_query
            1430,  # total_results
            10,  # num_results
            1,  # page_number
            10,  # num_links
            'agrodoctor.ua',  # visible_link
            'Length - 172MM. OEM #670120.1'  # snippet
        ))

        self._test_engine_normal('bing', 'data/uncompressed_2017/bing_samsung_p11.html', Expect(
            False,  # no_results
            '98-107 of 32,200,000 results',  # results_for_query
            32200000,  # total_results
            10,  # num_results
            11,  # page_number
            10,  # num_links
            'www.microsoft.com',  # visible_link
            'latest cell phones and smartphones'  # snippet
        ))

        self._test_engine_not_found('bing', 'data/uncompressed_2017/bing_not_found.html')

    # baidu
    def test_baidu(self):
        self._test_engine_normal('baidu', 'data/uncompressed_2017/baidu_670120.1_p1.html', Expect(
            False,                        # no_results
            '百度为您找到相关结果约3,240个',  # results_for_query
            3240,                         # total_results
            10,                           # num_results
            1,                            # page_number
            10,                           # num_links
            'www.76zh.com',               # visible_link
            '数学教育 670105K 数'           # snippet
        ))

        self._test_engine_normal('baidu', 'data/uncompressed_2017/baidu_samsung_p5.html', Expect(
            False,                            # no_results
            '百度为您找到相关结果约15,100,000个',  # results_for_query
            15100000,                         # total_results
            10,                               # num_results
            5,                                # page_number
            10,                               # num_links
            'account.samsung.com',            # visible_link
            '三星SDS的官'                       # snippet
        ))

        self._test_engine_not_found('baidu', 'data/uncompressed_2017/baidu_not_found.html')
