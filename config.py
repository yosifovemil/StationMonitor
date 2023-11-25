import configparser
import os


class Config:
    def __init__(self):
        parser = self.read_config()

        self._url = parser['Default']['URL'].strip()
        self._graphs = parser['Default']['Graphs'].split(" ")
        self._data_location = parser['Default']['DataLocation']
        self._last_updated_file = parser['Default']['LastUpdatedFile']

        self._email_user = parser['Gmail']['username']
        self._email_password = parser['Gmail']['password']
        self._admins = parser['Gmail']['admins'].split(" ")
        self._users = parser['Gmail']['users'].split(" ")

        self._single_exposure_limits = parser['SingleExposureLimits']
        self._avg_daily_limits = parser['AverageDailyLimits']

    def get_url(self):
        return self._url

    def get_graphs(self):
        return self._graphs

    def get_data_location(self):
        return self._data_location

    def get_last_updated_file(self):
        return self._last_updated_file

    def get_email_user(self):
        return self._email_user

    def get_email_password(self):
        return self._email_password

    def get_admins(self):
        return self._admins

    def get_users(self):
        return self._users

    def get_single_exposure_limit(self, compound):
        return float(self._single_exposure_limits[compound])

    def get_avg_daily_limit(self, compound):
        return float(self._avg_daily_limits[compound])

    def read_config(self):
        parser = configparser.ConfigParser()

        settings_file = os.path.join(os.path.expanduser("~"), "Config", "StationMonitor.ini")
        parser.read(settings_file)
        return parser
