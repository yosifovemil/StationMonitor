import configparser


class Config:
    def __init__(self):
        parser = self.read_config()

        self._url = parser['Default']['URL'].strip()
        self._graphs = parser['Default']['Graphs'].split(" ")
        self._data_location = parser['Default']['DataLocation']

    def get_url(self):
        return self._url

    def get_graphs(self):
        return self._graphs

    def get_data_location(self):
        return self._data_location

    def read_config(self):
        parser = configparser.ConfigParser()
        parser.read('settings.ini')
        return parser
