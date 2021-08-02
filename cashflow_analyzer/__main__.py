from cashflow_analyzer.requests import AnalyseRequest, AnalyseRequestValidator
from loader import *
from transactions import TRANSACTIONS_TYPES, TransactionsAnalyser
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='analyse account.')
    parser.add_argument('-t', '--transaction-type', type=str,
                        help=f'type of transaction from {list(TRANSACTIONS_TYPES.keys())}')
    parser.add_argument('-s', '--step', default="yearly", type=str,
                        help=f'monthly or yearly')

    parser.add_argument('-g', '--grouped', default=False, type=bool,
                        help=f'per group of payers/receiver')

    parser.add_argument('-p', '--payers', default="", type=str, nargs='+',
                        help=f'receiver/payer')

    args = parser.parse_args()
    request = AnalyseRequest(**vars(args))
    v = AnalyseRequestValidator()
    v.validate(request)

    PATH_DATA = r"../data/20210613-101728580-umsatz (1).CSV"
    # PATH_DATA = r"../data/Transactions_380_633854500_20210725_163342.csv"

    data = sparkasse_convertor(get_data(PATH_DATA))

    t = TransactionsAnalyser(transaction_type=request.transaction_type,
                             step=request.step,
                             is_grouped=request.grouped,
                             selections=request.payers)
    print(t.sum(data))
    if len(t.errors) != 0:
        print(t.errors)
