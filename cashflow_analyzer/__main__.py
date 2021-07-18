import pandas as pd
from loader import *
from calculate_cashflow import *


if __name__ == "__main__":
    PATH_DATA = r"../data/20210613-101728580-umsatz (1).CSV"

    data = get_data(PATH_DATA)
    print("cashflow")
    print(calculate_cashflow_every_month(filter_columns(data.copy())))

    print("revenus:")
    print(get_grouped_revenus_every_year(data.copy()))
    print(get_revenus_each_year(data.copy()))

    print("expenses:")
    print(get_grouped_expenses_every_month(data))
    print(get_expenses_each_year(data.copy()))
