import numpy as np

from cashflow_analyzer.requests import AnalyseRequest, AnalyseRequestValidator
from loader import *
from transactions import TRANSACTIONS_TYPES, TransactionsAnalyser
import argparse

import matplotlib.pyplot as plt


def plot_report_over_the_years(request):
    fig, ax = plt.subplots(figsize=(10, 5), tight_layout=True)
    ax.plot(result["years"], result["Betrag"], '-X')
    ax.set_xlabel("years")
    ax.set_ylabel(f"{request.transaction_type} in euro")
    ax.set_title(f"{request.transaction_type} over the years")
    plt.grid()
    plt.xticks(result["years"])
    plt.show()


def plot_report_over_the_month(request):
    result["date"] = result["years"].astype(str) + "-" + result["months"].astype(str)
    fig, ax = plt.subplots(figsize=(10, 5), tight_layout=True)

    ax.plot(result["date"], result["Betrag"], '-X')
    ax.set_xlabel("months")
    ax.set_ylabel(f"{request.transaction_type} in euro")
    ax.set_title(f"{request.transaction_type} over the months")
    plt.grid()
    plt.xticks(result["date"], rotation='vertical')
    plt.show()


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
    result = t.sum(data)
    print(result)
    if len(t.errors) != 0:
        print(t.errors)

    plot_report_over_the_month(request)
