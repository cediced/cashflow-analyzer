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
    return Revenus(data).get_grouped_by_year()


def get_revenus_each_year(data):
    return Revenus(data).get_transactions_by_year()


def get_grouped_expenses_every_year(data):
    return Expenses(data).get_grouped_by_year()


def get_expenses_each_year(data):
    return Expenses(data).get_transactions_by_year()


class Revenus:
    def __init__(self, data):
        self.data = data
        self.day = SCHEMA["day"]
        self.amount = SCHEMA["amount"]
        self.payer = "Beguenstigter/Zahlungspflichtiger"

    def filter_transaction(self, data):
        return data[data[SCHEMA["amount"]] > 0]

    def get_grouped_by_year(self):
        data = self.data[[self.day, self.amount, self.payer]]
        data.index = pd.to_datetime(data[self.day], format='%d.%m.%y')
        data[self.amount] = data[self.amount].str.replace(",", ".").astype(float)

        data = self.filter_transaction(data)

        return data.groupby(by=[data.index.year, self.payer]).sum().reset_index()

    def get_transactions_by_year(self):
        data = self.data[[self.day, self.amount]]
        data.index = pd.to_datetime(data[SCHEMA["day"]], format='%d.%m.%y')
        data[self.amount] = data[self.amount].str.replace(",", ".").astype(float)

        data = self.filter_transaction(data)

        return data.groupby(by=[data.index.year]).sum().reset_index()


class Expenses(Revenus):
    def __init__(self, data):
        super().__init__(data)

    def filter_transaction(self, data):
        return data[data[SCHEMA["amount"]] < 0]
