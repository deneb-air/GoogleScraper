# -*- coding: utf-8 -*-

import os
import unittest
from collections import namedtuple

# from SearchAnalyzer import scrape_with_config
from SearchAnalyzer.config import get_config
from SearchAnalyzer.parser.tools import get_parser_by_search_engine

Expect = namedtuple('Expect', [
    'results_for_query',
    'total_results',
    'num_results',
    'page_number',
    'no_results',
    'num_links'
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

    def _test_engine_normal(self, se, filename, expect):
        parser = self.get_parser_for_file(se, filename)

        self.assertFalse(expect.no_results)
        self.assertIn(expect.results_for_query, parser.num_results_for_query)
        self.assertEqual(expect.total_results, parser.total_results)
        self.assertEqual(expect.num_results, parser.num_results)
        self.assertEqual(expect.page_number, parser.page_number)
        self.assertEqual(expect.num_links, len(parser.search_results['results']))

    def test_google_normal(self):
        self._test_engine_normal('google', 'data/uncompressed_2017/google_670120.1_p1.html', Expect(
            'About 540 results (0.26 seconds)',  # results_for_query
            540,    # total_results
            9,      # num_results
            1,      # page_number
            False,  # no_results
            9       # num_links
        ))

        self._test_engine_normal('google', 'data/uncompressed_2017/google_samsung_p7.html', Expect(
            'Page 7 of about 1,470,000,000 results (0.77 seconds)',  # results_for_query
            1470000000,  # total_results
            13,          # num_results
            7,           # page_number
            False,       # no_results
            10           # num_links
        ))
