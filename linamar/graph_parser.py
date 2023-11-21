import pandas as pd


def parse(graph: str):
    """ Parses the graph data from the graph's HTML source
    :param graph: HTML source for the graph
    :return: Pandas dataframe containing the data
    """
    start_index = graph.find("DateTime")
    end_index = graph.find("{")
    graph = graph[start_index:end_index]

    end_index = graph.find(",\r\n")
    graph = graph[:end_index]

    rows = graph \
        .strip() \
        .replace('"', '') \
        .split("\\n+\r\n")

    colnames = rows[0].split(",")

    dates = []
    values = []
    for row in rows[1:]:
        row_vals = row.split(",")
        dates.append(row_vals[0])
        values.append(float(row_vals[1]))

    data = pd.DataFrame(data=list(zip(dates, values)), columns=colnames)
    data['DateTime'] = pd.to_datetime(data['DateTime'], format="%Y/%m/%d %H:%M:%S")
    return data
