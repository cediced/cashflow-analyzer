from cashflow_analyzer.presentation import graph_interface, to_pdfs
from cashflow_analyzer.requests import AnalyseRequest, AnalyseRequestValidator
from loader import *
from transactions import TransactionsAnalyser

from collections import namedtuple

Model = namedtuple("Model", "fig_size, amount, x_axis, x_label, y_label, title")

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
    models = []

    for request in requests:
        v = AnalyseRequestValidator()
        v.validate(request)

        t = TransactionsAnalyser(transaction_type=request.transaction_type,
                                 step=request.step,
                                 is_grouped=request.grouped,
                                 selections=request.payers)
        result = t.sum(data)

        models.append(graph_interface(result, request.transaction_type, request.step))

    to_pdfs(models, "../data/report.pdf")
