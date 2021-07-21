import pandas as pd

from cashflow_analyzer import calculate_cashflow as sut


def test_calculate_cashflow_for_every_month():
    transactions = pd.DataFrame(
        {"Buchungstag": ['01.01.18', '02.01.18', '04.05.18', '15.05.18', '04.02.19', '18.06.19', '20.06.19'],
         "Betrag": ["100", "200", "300,5", "-100", "10,75", "-5", "10"]})

    result = {'Betrag': [300.0, 200.5, 10.75, 5.0],
              'years': [2018, 2018, 2019, 2019],
              'months': [1, 5, 2, 6]}

    assert result == sut.calculate_cashflow_every_month(sut.filter_columns(transactions)).to_dict('list')


def test_retrieve_all_the_revenus_by_year_and_give_the_total():
    transactions = pd.DataFrame(
        {"Buchungstag": ['01.01.18', '02.01.18', '04.05.18', '15.05.18', '04.02.19', '18.06.19', '20.06.19'],
         "Betrag": ["100", "200", "300,5", "-100", "10,75", "-5", "10"],
         "Beguenstigter/Zahlungspflichtiger": ["VW", "Titi", "VW", "Supermarkt", "VW", "travel", "VW"]})

    result = {'Buchungstag': [2018, 2018, 2019],
              'Beguenstigter/Zahlungspflichtiger': ['Titi', 'VW', 'VW'],
              'Betrag': [200.0, 400.5, 20.75]}
    assert result == sut.get_grouped_revenus_every_year(transactions).to_dict('list')


def test_get_the_revenus_for_each_year():
    transactions = pd.DataFrame(
        {"Buchungstag": ['01.01.18', '02.01.18', '04.05.18', '15.05.18', '04.02.19', '18.06.19', '20.06.19'],
         "Betrag": ["100", "200", "300,5", "-100", "10,75", "-5", "10"]})

    result = {'Buchungstag': [2018, 2019],
              'Betrag': [600.5, 20.75]}
    assert result == sut.get_revenus_each_year(transactions).to_dict('list')


def test_retrieve_all_the_expenses_by_year():
    transactions = pd.DataFrame(
        {"Buchungstag": ['01.01.18', '02.01.18', '04.05.18', '15.05.18', '04.02.19', '18.06.19', '20.06.19', '20.06.19',
                         '20.06.19'],
         "Betrag": ["100", "200", "300,5", "-100", "10,75", "-5", "10", '-220', '-30.0'],
         "Beguenstigter/Zahlungspflichtiger": ["VW", "Titi", "VW", "Supermarkt", "VW", "travel", "VW", "travel",
                                               "Supermarkt"]
         })

    result = {'Buchungstag': [2018, 2019, 2019],
              'Beguenstigter/Zahlungspflichtiger': ['Supermarkt', 'Supermarkt', 'travel'],
              'Betrag': [-100.0, -30.0, -225.0]}
    assert result == sut.get_grouped_expenses_every_year(transactions).to_dict('list')


def test_get_the_expenses_for_each_year():
    transactions = pd.DataFrame(
        {"Buchungstag": ['01.01.18', '02.01.18', '04.05.18', '15.05.18', '04.02.19', '18.06.19', '20.06.19', '20.07.19', '20.06.19'],
         "Betrag": ["100", "200", "300,5", "-100", "10,75", "-5", "10", '-220', '-30']})

    result = {'Buchungstag': [2018, 2019],
              'Betrag': [-100, -255]}
    assert result == sut.get_expenses_each_year(transactions).to_dict('list')
