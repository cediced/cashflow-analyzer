from loader import *
from transactions import TRANSACTIONS_TYPE, TransactionsAnalyser
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='analyse account.')
    parser.add_argument('-t', '--transaction-type', type=str,
                        help=f'type of transaction from {list(TRANSACTIONS_TYPE.keys())}')
    parser.add_argument('-s', '--step', default="yearly", type=str,
                        help=f'monthly or yearly')

    parser.add_argument('-g', '--grouped', default=False, type=bool,
                        help=f'per group of payers/receiver')

    parser.add_argument('-p', '--payers', default="", type=str, nargs='+',
                        help=f'receiver/payer')


    args = parser.parse_args()


    PATH_DATA = r"../data/20210613-101728580-umsatz (1).CSV"

    data = get_data(PATH_DATA)

    transaction_type = args.transaction_type
    step = args.step
    grouped = args.grouped
    selections = args.payers

    t = TransactionsAnalyser(transaction_type, step, grouped, selections)
    print(t.sum(data))
    if len(t.errors) != 0:
        print(t.errors)
