from config import Config
import os
import pandas as pd
from analysis.analyzer import single_exposure_analysis


def load_files():
    csv_path = os.path.join("data", "csv")
    data = dict()
    for fname in os.listdir(csv_path):
        compound = fname.replace(".csv", "")
        df = pd.read_csv(os.path.join(csv_path, fname))
        df['DateTime'] = pd.to_datetime(df['DateTime'])
        data[compound] = df

    return data


def analyze_daily_averages(data: dict[str, pd.DataFrame], config: Config):
    above_limits = dict()

    for compound in data.keys():
        df = data[compound].resample('D', on='DateTime').mean().reset_index()
        limit = config.get_avg_daily_limit(compound)

        averages_above_limit = df[df[compound] >= limit]
        if len(averages_above_limit) > 0:
            above_limits[compound] = averages_above_limit

    return above_limits


def main():
    cfg = Config()

    data = load_files()

    daily_averages = analyze_daily_averages(data, cfg)
    if len(daily_averages) > 0:
        print("DAILY AVERAGES")
        for compound in daily_averages.keys():
            print(compound)
            print(daily_averages[compound].to_markdown(index=False))

    single_exposures = single_exposure_analysis(data, cfg)
    if len(single_exposures) > 0:
        print("SINGLE EXPOSURES")
        for compound in single_exposures.keys():
            print(compound)
            print(single_exposures[compound].to_markdown(index=False))


if __name__ == "__main__":
    main()
