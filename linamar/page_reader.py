import requests
from bs4 import BeautifulSoup
from linamar import graph_parser
from config import Config
import logging
from datetime import datetime
from file_io import filename_generator
import re
from email_client import error_message_admins


class PageReader:
    def __init__(self, config: Config):
        self._config = config
        self._soup = self.read_page()

    def snapshot_page(self):
        """ Saves webpage to html
        :return:
        """
        filename = filename_generator.generate(self._config, "snapshot", "html")

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(str(self._soup))
            f.flush()

    def fetch_graphs(self):
        """ Reads each graph's data into a Pandas dataframe
        :return: A dict of graph names and Pandas dataframes
        """
        graphs = self.fetch_graphs_as_str()
        dataframes = {}

        for graph_name in self._config.get_graphs():
            matching_graphs = [graph for graph in graphs if graph.find(graph_name) != -1]
            if len(matching_graphs) != 1:
                logging.warning("Unexpected number of graphs {num}".format(num=len(matching_graphs)))
            else:
                data = graph_parser.parse(matching_graphs[0])
                dataframes[graph_name] = data

        return dataframes

    def get_last_update(self):
        """Fetches date the graph was updated
        :return: Date when the graph was last updated
        """
        span_elements = self._soup.find_all(name="span")
        matching_elements = [elem.text for elem in span_elements if elem.text.find("Последна актуализация") != -1]

        if len(matching_elements) != 1:
            message = "Unexpected number of matching span elements {num} for last updated date".format(
                num=len(matching_elements))
            error_message_admins(message, self._config)
        else:
            elem = matching_elements[0]
            matched_date = re.search("\d\d\.\d\d\.\d\d\d\d \d\d:\d\d", elem)
            if matched_date is None:
                message = "Could not extract date from element {elem}".format(elem=elem)
                error_message_admins(message, self._config)
            else:
                return datetime.strptime(matched_date.group(), "%d.%m.%Y %H:%M")

    def read_page(self):
        session = requests.Session()
        page = session.get(self._config.get_url())
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup

    def fetch_graphs_as_str(self):
        scripts = []
        for script in self._soup.find_all('script'):
            script = str(script)
            if script.find("new Dygraph(document.getElementById") != -1:
                scripts.append(script)

        return scripts
