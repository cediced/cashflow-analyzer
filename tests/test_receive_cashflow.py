import pandas as pd


from cashflow_analyzer import calculate_cashflow as sut


def test_calculate_cashflow_for_every_month():
    transactions = pd.DataFrame(
        {"Buchungstag": ['01.01.18', '02.01.18', '04.05.18', '15.05.18', '04.02.19', '18.06.19', '20.06.19'],
         "Betrag": ["100", "200", "300,5", "-100", "10,75", "-5", "10"]})

    result = {'Betrag': {0: 300.0, 1: 200.5, 2: 10.75, 3: 5.0},
              'years': {0: 2018, 1: 2018, 2: 2019, 3: 2019},
              'months': {0: 1, 1: 5, 2: 2, 3: 6}}

    assert result == sut.calculate_cashflow_every_month(sut.filter_columns(transactions)).to_dict()
