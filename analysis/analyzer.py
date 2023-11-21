import pandas as pd

from config import Config
from email_client import notify_users


def analyze_and_notify(data: dict[str, pd.DataFrame], config: Config):
    single_exposures = single_exposure_analysis(data, config)
    averages = daily_average_analysis(data, config)

    if len(single_exposures) > 0 or len(averages) > 0:
        notify_users(single_exposures, averages, config)


def single_exposure_analysis(data: dict[str, pd.DataFrame], config: Config):
    compounds_over_limit = dict()
    for compound in data.keys():
        limit = config.get_single_exposure_limit(compound)

        readings_over_limit = data[compound][data[compound][compound] >= limit]
        if readings_over_limit.count()[compound] > 0:
            compounds_over_limit[compound] = readings_over_limit

    return compounds_over_limit


def daily_average_analysis(data: dict[str, pd.DataFrame], config: Config):
    compounds_over_limit = dict()
    for compound in data.keys():
        limit = config.get_avg_daily_limit(compound)

        average = data[compound][compound].mean()

        if average > limit:
            compounds_over_limit[compound] = average

    return compounds_over_limit
