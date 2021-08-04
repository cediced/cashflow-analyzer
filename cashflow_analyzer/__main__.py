import numpy as np

from cashflow_analyzer.requests import AnalyseRequest, AnalyseRequestValidator
from loader import *
from transactions import TRANSACTIONS_TYPES, TransactionsAnalyser
import argparse

import matplotlib.pyplot as plt

from collections import namedtuple

Model = namedtuple("Model", "fig_size, amount, x_axis, x_label, y_label, title")


def graph_interface(data, transaction_type, step):
    step_title = "years" if step == "yearly" else "months"
    type = "cashflow" if transaction_type == "all" else transaction_type
    x_axis = data[step_title] if step == "yearly" else data["years"].astype(str) + "-" + data["months"].astype(str)

    return Model(fig_size=(10, 5),
                 amount=data[SCHEMA["amount"]],
                 x_axis=x_axis,
                 x_label=step_title,
                 y_label=f"{type} in euro",
                 title=f"{type} over the {step_title}")


def plot_report(model: Model):
    fig, ax = plt.subplots(figsize=model.fig_size, tight_layout=True)
    ax.plot(model.x_axis, model.amount, '-X')
    ax.set_xlabel(model.x_label)
    ax.set_ylabel(model.y_label)
    ax.set_title(model.title)
    plt.grid()
    plt.xticks(model.x_axis, rotation='vertical')


if __name__ == "__main__":

    PATH_DATA = r"../data/20210613-101728580-umsatz (1).CSV"
    # PATH_DATA = r"../data/Transactions_380_633854500_20210725_163342.csv"

    data = sparkasse_convertor(get_data(PATH_DATA))

    requests = [AnalyseRequest(transaction_type="all"),
                AnalyseRequest(transaction_type="expenses"),
                AnalyseRequest(transaction_type="revenues"),
                AnalyseRequest(transaction_type="all", step="monthly"),
                AnalyseRequest(transaction_type="expenses", step="monthly"),
                AnalyseRequest(transaction_type="revenues", step="monthly")
                ]

    for request in requests:
        v = AnalyseRequestValidator()
        v.validate(request)

        t = TransactionsAnalyser(transaction_type=request.transaction_type,
                                 step=request.step,
                                 is_grouped=request.grouped,
                                 selections=request.payers)
        result = t.sum(data)

        plot_report(graph_interface(result, request.transaction_type, request.step))
        plt.show()
