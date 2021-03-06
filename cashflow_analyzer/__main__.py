from cashflow_analyzer.config import CATEGORIES, RENAME
from cashflow_analyzer.presentation import graph_interface, to_pdfs, grouped_interface
from cashflow_analyzer.requests import AnalyseRequest, AnalyseRequestValidator
from loader import *
from transactions import TransactionsAnalyser, categorize, rename

if __name__ == "__main__":

    PATH_DATA = r"../data/20210613-101728580-umsatz (1).CSV"
    # PATH_DATA = r"../data/Transactions_380_633854500_20210725_163342.csv"

    years = [2020, 2021]
    data = categorize(sparkasse_convertor(get_data(PATH_DATA)), categories=CATEGORIES)

    requests = [AnalyseRequest(transaction_type="all"),
                AnalyseRequest(transaction_type="expenses"),
                AnalyseRequest(transaction_type="revenues"),
                AnalyseRequest(transaction_type="all", step="monthly"),
                AnalyseRequest(transaction_type="expenses", step="monthly"),
                AnalyseRequest(transaction_type="revenues", step="monthly"),
                AnalyseRequest(transaction_type="revenues", step="monthly", grouped=True),
                AnalyseRequest(transaction_type="expenses", step="monthly", grouped=True)
                ]
    models = []

    for request in requests:
        v = AnalyseRequestValidator()
        v.validate(request)

        t = TransactionsAnalyser(transaction_type=request.transaction_type,
                                 step=request.step,
                                 is_grouped=request.grouped,
                                 selections=request.payers,
                                 years=years)
        result = t.sum(data)
        print(result)

        if request.grouped:
            for model in grouped_interface(result, request.transaction_type, request.step):
                models.append(model)
        else:
            models.append(graph_interface(result, request.transaction_type, request.step))

    to_pdfs(models, f"../data/tmp/report_{str(years)}.pdf")
