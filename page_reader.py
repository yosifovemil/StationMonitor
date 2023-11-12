import requests
from bs4 import BeautifulSoup
import graph_parser
from config import Config
import logging
from datetime import datetime
import filename_generator


class PageReader:
    def __init__(self, config: Config):
        self._config = config
        self._soup = self.read_page()

    def snapshot_page(self):
        """ Saves webpage to html
        :param filename: path to the html file
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
