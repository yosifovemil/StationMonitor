from config import Config
import pandas as pd
import os


def write_to_file(config: Config, graphs: dict[str, pd.DataFrame]):
    for graph_name in graphs.keys():
        filename = os.path.join(config.get_data_location(), "csv", graph_name + ".csv")
        write_header = not os.path.exists(filename)
        graphs[graph_name].to_csv(filename, header=write_header, index=False, mode='a')
