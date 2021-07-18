"""
calculate the cashflow (difference entrance and lost for every month)
"""

import pandas as pd


def get_data(path_data):
    return pd.read_csv(path_data, sep=";")


def filter_columns(data):
    return data[["Buchungstag", "Betrag"]]


def calculate_cashflow_every_month(data):
    data.index = pd.to_datetime(data['Buchungstag'], format='%d.%m.%y')
    data["Betrag"] = data["Betrag"].str.replace(",", ".").astype(float)
    grouped = data.groupby(by=[data.index.year, data.index.month])
    summed = grouped.sum()

    summed["years"] = [group[0] for group in grouped.groups.keys()]
    summed["months"] = [group[1] for group in grouped.groups.keys()]
    summed.reset_index(drop=True, inplace=True)
    return summed
