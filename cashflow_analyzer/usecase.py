from dataclasses import dataclass
from collections import defaultdict
import pandas as pd


@dataclass
class Transaction:
    informations: list()


TRANSACTION = Transaction(informations=["dates", "amounts"])


class CalculateCashflow:
    def __init__(self, transactions):
        self.transactions = transactions
        self.errors = defaultdict(list)

    def execute(self):
        self.validate_transactions()

    def validate_transactions(self):
        if not isinstance(self.transactions, pd.DataFrame):
            self.errors["wrong_type_input"].append(f'transaction is {type(self.transactions)} '
                                                   f'instead of dataframe')
            return

        for column in list(self.transactions.columns):
            if column not in TRANSACTION.informations:
                self.errors["wrong_columns_information"].append(column)
            return


