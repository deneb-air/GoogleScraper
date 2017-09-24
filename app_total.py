#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Convenience wrapper for running GoogleScrapper directly from source tree."""

from xml.dom.minidom import getDOMImplementation

from SearchAnalyzer.commandline import get_command_line
from SearchAnalyzer.core import main

from app_total_conf import app_total_conf


class App:
    def __init__(self, config):
        cmd = get_command_line()
        kwfile = cmd.get('keyword_file')

        self.config = config
        self.config['keyword_file'] = kwfile

        self.output = kwfile.replace('.qry', '')
        self.output = self.output.replace('request', 'response')
        self.output += '.xml'

        self._serps = None
        self.data = {}

    def run(self):
        scrapper_search = main(True, False, self.config)
        self._serps = scrapper_search.serps

        self._parse_serps()

        return self.data

    def save(self):
        xml_doc = self._make_xml()

        ofile = open(self.output, 'wb')
        ofile.write(xml_doc.toprettyxml().encode('utf-8'))
        ofile.close()

        return xml_doc

    def _make_xml(self):
        impl = getDOMImplementation()

        xml_doc = impl.createDocument(None, 'root', None)
        xml_root = xml_doc.documentElement
        xml_items = xml_doc.createElement('items')
        for keyword in self.data:
            xml_item = xml_doc.createElement('item')

            xml_query = xml_doc.createElement('query')
            xml_query.appendChild(xml_doc.createTextNode(keyword))
            xml_item.appendChild(xml_query)

            xml_engines = xml_doc.createElement('engines')
            for engine in self.data[keyword]:
                xml_engine = App._create_engine_node(xml_doc, engine, data[keyword][engine])
                xml_engines.appendChild(xml_engine)

            xml_item.appendChild(xml_engines)
            xml_items.appendChild(xml_item)

        xml_root.appendChild(xml_items)

        return xml_doc

    @staticmethod
    def _create_engine_node(xml_doc, name, result):
        e = xml_doc.createElement('engine')

        n = xml_doc.createElement('name')
        s = xml_doc.createElement('status')
        t = xml_doc.createElement('total')

        n.appendChild(xml_doc.createTextNode(name))
        s.appendChild(xml_doc.createTextNode(result['status']))
        t.appendChild(xml_doc.createTextNode(str(result['total_results'])))

        e.appendChild(n)
        e.appendChild(s)
        e.appendChild(t)

        return e

    def _parse_serps(self):
        self.data = {}
        for search_res in self._serps:
            if search_res.query not in self.data:
                self.data[search_res.query] = {}
            if search_res.search_engine_name not in self.data[search_res.query]:
                self.data[search_res.query][search_res.search_engine_name] = {}

            self.data[search_res.query][search_res.search_engine_name]['status'] = search_res.status
            self.data[search_res.query][search_res.search_engine_name]['total_results'] = search_res.total_results


if __name__ == '__main__':
    sa = App(app_total_conf)
    data = sa.run()
    xml_d = sa.save()

    print("##########################################")
    print(xml_d.toprettyxml())
    print("##########################################")
