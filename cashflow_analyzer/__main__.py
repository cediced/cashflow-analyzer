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
    return summed


if __name__ == "__main__":
    PATH_DATA = r"../data/20210613-101728580-umsatz (1).CSV"

    data = get_data(PATH_DATA)
    print(calculate_cashflow_every_month(filter_columns(data)))
