import pandas as pd


def get_data(path_data):
    return pd.read_csv(path_data, sep=";")
