from loader import *
from transactions import TRANSACTIONS_TYPE, create_transactions

if __name__ == "__main__":
    PATH_DATA = r"../data/20210613-101728580-umsatz (1).CSV"

    data = get_data(PATH_DATA)
    transactions = list(TRANSACTIONS_TYPE.keys())
    while(1):

        transaction_type = input(f"what doy ou want to analyze? chose between, {transactions} : ")

        if transaction_type in transactions:
            transaction = create_transactions(transaction_type, data)
            print(transaction.monthly_cashflow())
        else:
            print(f"{transaction_type} is not {transactions}")
