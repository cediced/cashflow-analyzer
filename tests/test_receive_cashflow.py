import pandas as pd
import pytest

import cashflow_analyzer.transactions as sut


@pytest.fixture(name="transactions_creator")
def fixture_transactions_creator():
    return sut.create_transactions


DAY = sut.SCHEMA["day"]
AMOUNT = sut.SCHEMA["amount"]
PAYER = sut.SCHEMA["payer"]


def test_calculate_cashflow_for_every_month(transactions_creator):
    transactions = pd.DataFrame(
        {DAY: ['01.01.18', '02.01.18', '04.05.18', '15.05.18', '04.02.19', '18.06.19', '20.06.19'],
         AMOUNT: ["100", "200", "300,5", "-100", "10,75", "-5", "10"]})

    result = {AMOUNT: [300.0, 200.5, 10.75, 5.0],
              'years': [2018, 2018, 2019, 2019],
              'months': [1, 5, 2, 6]}

    assert result == transactions_creator("all", transactions).monthly_cashflow().to_dict('list')


def test_retrieve_all_the_revenus_by_year_and_give_the_total(transactions_creator):
    transactions = pd.DataFrame(
        {DAY: ['01.01.18', '02.01.18', '04.05.18', '15.05.18', '04.02.19', '18.06.19', '20.06.19'],
         AMOUNT: ["100", "200", "300,5", "-100", "10,75", "-5", "10"],
         PAYER: ["VW", "Titi", "VW", "Supermarkt", "VW", "travel", "VW"]})

    result = {'Buchungstag': [2018, 2018, 2019],
              'Beguenstigter/Zahlungspflichtiger': ['Titi', 'VW', 'VW'],
              'Betrag': [200.0, 400.5, 20.75]}
    assert result == transactions_creator("revenus", transactions).get_grouped_by_year().to_dict('list')


def test_get_the_revenus_for_each_year(transactions_creator):
    transactions = pd.DataFrame(
        {DAY: ['01.01.18', '02.01.18', '04.05.18', '15.05.18', '04.02.19', '18.06.19', '20.06.19'],
         AMOUNT: ["100", "200", "300,5", "-100", "10,75", "-5", "10"]})

    result = {'Buchungstag': [2018, 2019],
              'Betrag': [600.5, 20.75]}
    assert result == transactions_creator("revenus", transactions).get_transactions_by_year().to_dict('list')


def test_retrieve_all_the_expenses_by_year(transactions_creator):
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
    assert result == transactions_creator("expenses", transactions).get_grouped_by_year().to_dict('list')


def test_get_the_expenses_for_each_year(transactions_creator):
    transactions = pd.DataFrame(
        {DAY: ['01.01.18', '02.01.18', '04.05.18', '15.05.18', '04.02.19', '18.06.19', '20.06.19', '20.07.19',
               '20.06.19'],
         AMOUNT: ["100", "200", "300,5", "-100", "10,75", "-5", "10", '-220', '-30']})

    result = {'Buchungstag': [2018, 2019],
              'Betrag': [-100, -255]}
    assert result == result == transactions_creator("expenses", transactions).get_transactions_by_year().to_dict('list')
