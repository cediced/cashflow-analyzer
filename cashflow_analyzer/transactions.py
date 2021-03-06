from abc import ABC

import numpy as np
import pandas as pd

SCHEMA = {"day": "Buchungstag",
          "amount": "Betrag",
          "payer": "Beguenstigter/Zahlungspflichtiger",
          "category": "category"}

DAY_FORMAT = '%d.%m.%y'
STEP_TYPES = {"monthly": "monthly",
              "yearly": "yearly"}


class Transactions(ABC):
    def __init__(self, data):
        self.data = data.copy()
        self.day = SCHEMA["day"]
        self.amount = SCHEMA["amount"]
        self.payer = SCHEMA["payer"]
        self.category = SCHEMA["category"]
        self.data.index = pd.to_datetime(data[self.day], format="%d.%m.%Y")

    def filter_transactions(self, data):
        return data

    def sum_by_year_grouped(self, selections=None):
        data = self.data[[self.day, self.amount, self.payer]]

        data = self.filter_replace_payer_according_to_selection(selections, data.copy())

        data = self.process_data(data)
        return data.groupby(by=[data.index.year, self.payer]).sum().reset_index()

    def sum_by_month_grouped(self, selections=None):
        data = self.data[[self.day, self.amount, self.payer]]

        data = self.filter_replace_payer_according_to_selection(selections, data.copy())

        data = self.process_data(data)
        grouped = data.groupby(by=[data.index.year, data.index.month, self.payer])
        summed = grouped.sum()
        summed = summed.rename_axis(['years', 'month', SCHEMA['payer']]).reset_index()
        return summed

    def sum_by_year(self):
        data = self.data[[self.day, self.amount]]
        data = self.process_data(data)
        data = data.groupby(by=[data.index.year]).sum().reset_index()
        data = data.rename(columns={self.day: "years"})
        return data

    def sum_by_month(self):
        data = self.data.copy()
        data = data[[self.amount, self.day]]

        data = self.filter_transactions(data)

        grouped = data.groupby(by=[data.index.year, data.index.month])
        summed = grouped.sum()

        summed["years"] = [group[0] for group in grouped.groups.keys()]
        summed["months"] = [group[1] for group in grouped.groups.keys()]
        summed.reset_index(drop=True, inplace=True)
        return summed

    def process_data(self, data):
        data = self.filter_transactions(data)
        return data

    def filter_replace_payer_according_to_selection(self, selections, df):
        if selections:
            df = df[df[self.payer].str.contains('|'.join(selections), na=False)]

            for selection in selections:
                df.loc[df[self.payer].str.contains(selection, na=False), self.payer] = selection
        return df


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


TRANSACTIONS_TYPES = {"all": Transactions,
                      "revenues": Revenues,
                      "expenses": Expenses}


class NotDefinedTransactionTypeError(Exception):
    pass


class TransactionsAnalyser:
    def __init__(self, transaction_type, step=STEP_TYPES["yearly"], is_grouped=False, selections=None, years=None):
        self.errors = []
        self.transaction_type = transaction_type
        self.step = step
        self.is_grouped = is_grouped
        self.selections = selections if selections else []
        self.years = years

    def sum(self, data: pd.DataFrame):
        result = None

        transaction = self.create_transactions(self.transaction_type.lower(), data)

        if self.step == STEP_TYPES["yearly"] and self.is_grouped:
            result = transaction.sum_by_year_grouped(selections=self.selections)
        elif self.step == STEP_TYPES["yearly"]:
            result = transaction.sum_by_year()
        elif self.step == STEP_TYPES["monthly"] and self.is_grouped:
            result = transaction.sum_by_month_grouped(selections=self.selections)

            if self.years:
                result = result[result["years"].isin(self.years)]

        elif self.step == STEP_TYPES["monthly"]:
            result = transaction.sum_by_month()

            if self.years:
                result = result[result["years"].isin(self.years)]

        return result

    def create_transactions(self, type, data) -> Transactions:
        try:
            return TRANSACTIONS_TYPES[type](data)
        except KeyError as err:
            raise NotDefinedTransactionTypeError(
                f"{type} is not a valid transaction type, chose among {list(TRANSACTIONS_TYPES.keys())}") from err


def categorize(transactions: pd.DataFrame, categories: dict) -> pd.DataFrame:
    result = transactions.copy()

    categories_low = dict((k.lower(), list(map(str.lower, v))) for k,v in categories.items())

    result['category'] = "other"
    for catego, values in categories_low.items():
        result['category'] = np.where(result[SCHEMA["payer"]].str.lower().str.contains("|".join(values)),
                                      catego,
                                      result['category'])
    return result


def rename(df: pd.DataFrame, column: str, mapping: list):
    for selection in mapping:
        df.loc[df[column].str.contains(selection, na=False), column] = selection
