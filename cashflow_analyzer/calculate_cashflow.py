"""
calculate the cashflow (difference entrance and lost for every month)
"""

import pandas as pd

SCHEMA = {"day": "Buchungstag",
          "amount": "Betrag"}


def filter_columns(data):
    return data[SCHEMA.values()]


def calculate_cashflow_every_month(data):
    data.index = pd.to_datetime(data[SCHEMA["day"]], format='%d.%m.%y')
    data[SCHEMA["amount"]] = data[SCHEMA["amount"]].str.replace(",", ".").astype(float)
    grouped = data.groupby(by=[data.index.year, data.index.month])
    summed = grouped.sum()

    summed["years"] = [group[0] for group in grouped.groups.keys()]
    summed["months"] = [group[1] for group in grouped.groups.keys()]
    summed.reset_index(drop=True, inplace=True)
    return summed


def get_grouped_revenus_every_year(data):
    return get_grouped_transactions_by_year("revenus", data)


def get_grouped_transactions_by_year(type_of_transaction, data):
    day = SCHEMA["day"]
    amount = SCHEMA["amount"]
    payer = "Beguenstigter/Zahlungspflichtiger"
    data = data[[day, amount, payer]]
    data.index = pd.to_datetime(data[SCHEMA["day"]], format='%d.%m.%y')
    data[amount] = data[amount].str.replace(",", ".").astype(float)

    if type_of_transaction == "revenus":
        data = data[data[amount] > 0]
    else:
        data = data[data[amount] < 0]

    return data.groupby(by=[data.index.year, payer]).sum().reset_index()


def get_revenus_each_year(data):
    return get_transactions_by_year("revenus", data)


def get_transactions_by_year(type_of_transaction, data):
    day = SCHEMA["day"]
    amount = SCHEMA["amount"]
    data = data[[day, amount]]
    data.index = pd.to_datetime(data[SCHEMA["day"]], format='%d.%m.%y')
    data[amount] = data[amount].str.replace(",", ".").astype(float)

    if type_of_transaction == "revenus":
        data = data[data[amount] > 0]
    else:
        data = data[data[amount] < 0]

    return data.groupby(by=[data.index.year]).sum().reset_index()


def get_grouped_expenses_every_month(data):
    return get_grouped_transactions_by_year("expenses", data)


def get_expenses_each_year(data):
    return get_transactions_by_year("expenses", data)
