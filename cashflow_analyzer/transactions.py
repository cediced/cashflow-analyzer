from abc import ABC
import pandas as pd

SCHEMA = {"day": "Buchungstag",
          "amount": "Betrag",
          "payer": "Beguenstigter/Zahlungspflichtiger"}

DAY_FORMAT = '%d.%m.%y'
STEP_TYPES = {"monthly": "monthly",
              "yearly": "yearly"}


class Transactions(ABC):
    def __init__(self, data):
        self.data = data.copy()
        self.day = SCHEMA["day"]
        self.amount = SCHEMA["amount"]
        self.payer = SCHEMA["payer"]
        self.data.index = pd.to_datetime(data[self.day], format="%d.%m.%Y")

    def filter_transactions(self, data):
        return data

    def sum_by_year_grouped(self):
        data = self.data[[self.day, self.amount, self.payer]]
        data = self.process_data(data)
        return data.groupby(by=[data.index.year, self.payer]).sum().reset_index()

    def sum_by_month_grouped(self):
        data = self.data[[self.day, self.amount, self.payer]]
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
    def __init__(self, transaction_type, step=STEP_TYPES["yearly"], is_grouped=False, selections=None):
        self.errors = []
        self.transaction_type = transaction_type
        self.step = step
        self.is_grouped = is_grouped
        self.selections = selections if selections else []

    def sum(self, data: pd.DataFrame):
        result = None

        self.validate_step()
        transaction = self.create_transactions(self.transaction_type.lower(), data)

        if self.step == STEP_TYPES["yearly"] and self.is_grouped:
            result = transaction.sum_by_year_grouped()
        elif self.step == STEP_TYPES["yearly"]:
            result = transaction.sum_by_year()
        elif self.step == STEP_TYPES["monthly"] and self.is_grouped:
            result = transaction.sum_by_month_grouped()
        elif self.step == STEP_TYPES["monthly"]:
            result = transaction.sum_by_month()

        if len(self.selections) > 0 and SCHEMA["payer"] in result.columns:
            result = result[result[SCHEMA["payer"]].str.contains('|'.join(self.selections))]

        return result

    def validate_step(self):
        valids_steps = STEP_TYPES.keys()
        if self.step not in valids_steps:
            self.errors.append(f"{self.step} was not in {valids_steps}")

    def create_transactions(self, type, data) -> Transactions:
        try:
            return TRANSACTIONS_TYPES[type](data)
        except KeyError as err:
            raise NotDefinedTransactionTypeError(
                f"{type} is not a valid transaction type, chose among {list(TRANSACTIONS_TYPES.keys())}") from err
