from abc import ABC

import pandas as pd

SCHEMA = {"day": "Buchungstag",
          "amount": "Betrag",
          "payer": "Beguenstigter/Zahlungspflichtiger"}


class Transactions(ABC):
    def __init__(self, data):
        self.data = data
        self.day = SCHEMA["day"]
        self.amount = SCHEMA["amount"]
        self.payer = SCHEMA["payer"]

    def filter_transactions(self, data):
        return data

    def sum_by_year_grouped(self):
        data = self.data[[self.day, self.amount, self.payer]]
        data = self.process_data(data)
        return data.groupby(by=[data.index.year, self.payer]).sum().reset_index()

    def sum_by_year(self):
        data = self.data[[self.day, self.amount]]
        data = self.process_data(data)
        data = data.groupby(by=[data.index.year]).sum().reset_index()
        data = data.rename(columns={self.day: "years"})
        return data

    def sum_by_month_grouped(self):
        data = self.data[[self.day, self.amount, self.payer]]
        data = self.process_data(data)
        grouped = data.groupby(by=[data.index.year, data.index.month, self.payer])
        summed = grouped.sum()

        summed["years"] = [group[0] for group in grouped.groups.keys()]
        summed["months"] = [group[1] for group in grouped.groups.keys()]
        summed["payer"] = [group[2] for group in grouped.groups.keys()]

        summed.reset_index(drop=True, inplace=True)
        return summed

    def sum_by_month(self):
        data = self.data.copy()
        data = data[[self.amount, self.day]]
        data.index = pd.to_datetime(data[self.day], format='%d.%m.%y')
        data[self.amount] = data[self.amount].str.replace(",", ".").astype(float)

        data = self.filter_transactions(data)

        grouped = data.groupby(by=[data.index.year, data.index.month])
        summed = grouped.sum()

        summed["years"] = [group[0] for group in grouped.groups.keys()]
        summed["months"] = [group[1] for group in grouped.groups.keys()]
        summed.reset_index(drop=True, inplace=True)
        return summed

    def process_data(self, data):
        data.index = pd.to_datetime(data[self.day], format='%d.%m.%y')
        data[self.amount] = data[self.amount].str.replace(",", ".").astype(float)
        data = self.filter_transactions(data)
        return data


class Revenues(Transactions):
    def __init__(self, data):
        super().__init__(data)

    def filter_transactions(self, data):
        return data[data[SCHEMA["amount"]] > 0]


class Expenses(Transactions):
    def __init__(self, data):
        super().__init__(data)

    def filter_transactions(self, data):
        return data[data[SCHEMA["amount"]] < 0]


TRANSACTIONS_TYPE = {"all": Transactions,
                     "revenues": Revenues,
                     "expenses": Expenses}


def create_transactions(type, data) -> Transactions:
    type = type.lower()

    try:
        return TRANSACTIONS_TYPE[type](data)
    except KeyError as err:
        raise NotDefinedTransactionTypeError(
            f"{type} is not a valid transaction type, chose among {list(TRANSACTIONS_TYPE.keys())}") from err


class NotDefinedTransactionTypeError(Exception):
    pass
