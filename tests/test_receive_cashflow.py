import pandas as pd
import pytest

import cashflow_analyzer.transactions as sut
from cashflow_analyzer.loader import sparkasse_convertor

DAY = sut.SCHEMA["day"]
AMOUNT = sut.SCHEMA["amount"]
PAYER = sut.SCHEMA["payer"]


@pytest.fixture(name="convertor")
def fixture_convert():
    return sparkasse_convertor


def test_sum_all_by_month(convertor):
    transactions = pd.DataFrame(
        {DAY: ['01.01.18', '02.01.18', '04.05.18', '15.05.18', '04.02.19', '18.06.19', '20.06.19'],
         AMOUNT: ["100", "200", "300,5", "-100", "10,75", "-5", "10"],
         "not_important_column": [1, 2, 3, 4, 5, 6, 7],
         PAYER: ["VW", "Titi", "VW", "Supermarkt", "VW", "travel", "VW"]})

    result = {AMOUNT: [300.0, 200.5, 10.75, 5.0],
              'years': [2018, 2018, 2019, 2019],
              'months': [1, 5, 2, 6]}

    assert result == sut.TransactionsAnalyser("all", step="monthly").sum(convertor(transactions)).to_dict('list')


def test_sum_by_month_grouped(convertor):
    transactions = pd.DataFrame(
        {DAY: ['01.01.18', '03.01.18', '04.01.18', '15.01.18', '04.02.19', '18.02.19', '20.02.19'],
         AMOUNT: ["100", "200", "300,5", "-100", "10,75", "-5", "10"],
         PAYER: ["VW", "Titi", "VW", "Supermarkt", "VW", "travel", "VW"]})

    result = {'Betrag': [-100.0, 200.0, 400.5, 20.75, -5.0],
              'years': [2018, 2018, 2018, 2019, 2019],
              'month': [1, 1, 1, 2, 2],
              PAYER: ['Supermarkt', 'Titi', 'VW', 'VW', 'travel']}

    assert result == sut.TransactionsAnalyser("all", step="monthly", is_grouped=True).sum(
        convertor(transactions)).to_dict('list')


def test_sum_all_the_transactions_over_the_year(convertor):
    transactions = pd.DataFrame(
        {DAY: ['01.01.18', '02.01.18', '04.05.18', '15.05.18', '04.02.19', '18.06.19', '20.06.19'],
         AMOUNT: ["100", "200", "300,5", "-100", "10,75", "-5", "10"],
         "not_important_column": [1, 2, 3, 4, 5, 6, 7],
         PAYER: ["VW", "Titi", "VW", "Supermarkt", "VW", "travel", "VW"]})

    result = {AMOUNT: [500.5, 15.75],
              'years': [2018, 2019]}

    assert result == sut.TransactionsAnalyser("all").sum(convertor(transactions)).to_dict('list')


def test_retrieve_all_the_revenues_by_year_and_give_the_total(convertor):
    transactions = pd.DataFrame(
        {DAY: ['01.01.18', '02.01.18', '04.05.18', '15.05.18', '04.02.19', '18.06.19', '20.06.19'],
         AMOUNT: ["100", "200", "300,5", "-100", "10,75", "-5", "10"],
         PAYER: ["VW", "Titi", "VW", "Supermarkt", "VW", "travel", "VW"]})

    result = {'Buchungstag': [2018, 2018, 2019],
              'Beguenstigter/Zahlungspflichtiger': ['Titi', 'VW', 'VW'],
              'Betrag': [200.0, 400.5, 20.75]}
    assert result == sut.TransactionsAnalyser("revenues", is_grouped=True).sum(convertor(transactions)).to_dict('list')


def test_get_the_revenues_for_each_year(convertor):
    transactions = pd.DataFrame(
        {DAY: ['01.01.18', '02.01.18', '04.05.18', '15.05.18', '04.02.19', '18.06.19', '20.06.19'],
         AMOUNT: ["100", "200", "300,5", "-100", "10,75", "-5", "10"],
         PAYER: ["VW", "Titi", "VW", "Supermarkt", "VW", "travel", "VW"]})

    result = {'years': [2018, 2019],
              'Betrag': [600.5, 20.75]}
    assert result == sut.TransactionsAnalyser("revenues").sum(convertor(transactions)).to_dict('list')


def test_retrieve_all_the_expenses_by_year(convertor):
    transactions = pd.DataFrame(
        {DAY: ['01.01.18', '02.01.18', '04.05.18', '15.05.18', '04.02.19', '18.06.19', '20.06.19', '20.06.19',
               '20.06.19'],
         AMOUNT: ["100", "200", "300,5", "-100", "10,75", "-5", "10", '-220', '-30.0'],
         PAYER: ["VW", "Titi", "VW", "Supermarkt", "VW", "travel", "VW", "travel",
                 "Supermarkt"]
         })

    result = {'Buchungstag': [2018, 2019, 2019],
              'Beguenstigter/Zahlungspflichtiger': ['Supermarkt', 'Supermarkt', 'travel'],
              'Betrag': [-100.0, -30.0, -225.0]}
    assert result == sut.TransactionsAnalyser("expenses", is_grouped=True).sum(convertor(transactions)).to_dict('list')


def test_get_the_expenses_for_each_year(convertor):
    transactions = pd.DataFrame(
        {DAY: ['01.01.18', '02.01.18', '04.05.18', '15.05.18', '04.02.19', '18.06.19', '20.06.19', '20.07.19',
               '20.06.19'],
         AMOUNT: ["100", "200", "300,5", "-100", "10,75", "-5", "10", '-220', '-30'],
         PAYER: ["VW", "Titi", "VW", "Supermarkt", "VW", "travel", "VW", "shop", "sport"]})

    result = {'years': [2018, 2019],
              'Betrag': [-100, -255]}
    assert result == sut.TransactionsAnalyser("expenses").sum(convertor(transactions)).to_dict('list')


def test_selections_of_groups(convertor):
    transactions = pd.DataFrame(
        {DAY: ['01.01.18', '02.01.18', '04.05.18', '15.05.18', '04.02.19', '18.06.19', '20.06.19', '20.06.19',
               '20.06.19'],
         AMOUNT: ["100", "200", "300,5", "-100", "10,75", "-5", "10", '-220', '-30.0'],
         PAYER: ["VW", "Titi", "VW", "Supermarkt", "VW", "travel", "VW", "travel",
                 "Supermarkt"]
         })
    selections = ["VW", "Supermarkt"]

    usecase = sut.TransactionsAnalyser("all", is_grouped=True, selections=selections)
    result = usecase.sum(convertor(transactions))
    assert set(result[PAYER].values).issubset(selections)
