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
    data = pd.DataFrame(
        {"Buchungstag": ['01.01.18', '02.01.18', '04.05.18', '15.05.18', '04.02.19', '18.06.19', '20.06.19'],
         "Betrag": ["100", "200", "300,5", "-100", "10,75", "-5", "10"]})
    print(calculate_cashflow_every_month(filter_columns(data)))
