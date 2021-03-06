import random

import numpy as np
from hypothesis import given, example, settings, reproduce_failure, HealthCheck
import hypothesis.strategies as st
import pandas as pd
import pytest

import cashflow_analyzer.transactions as sut
from cashflow_analyzer.requests import AnalyseRequest, AgumentsErrors, AnalyseRequestValidator
from cashflow_analyzer.transactions import TRANSACTIONS_TYPES

DAY = sut.SCHEMA["day"]
AMOUNT = sut.SCHEMA["amount"]
PAYER = sut.SCHEMA["payer"]
CATEGORIES = sut.SCHEMA["category"]


class TransactionsValues:
    def __init__(self):
        self.values = pd.DataFrame(
            {DAY: ['01.01.2018', '02.01.2018', '04.05.2018', '15.05.2018', '04.02.2019', '18.06.2019', '20.06.2019',
                   '20.06.2019',
                   '20.06.2019'],
             AMOUNT: [100, 200, 300.5, -100, 10.75, -5, 10, -220, -30.0],
             PAYER: ["VW", "Titi", "VW", "Supermarkt", "VW", "travel", "VW", "travel",
                     "Supermarkt"]
             })

    @property
    def amount_per_month(self):
        return {AMOUNT: [300.0, 200.5, 10.75, -245],
                'years': [2018, 2018, 2019, 2019],
                'months': [1, 5, 2, 6]}


@pytest.fixture(name="transactions")
def fixture_transactions():
    return pd.DataFrame(
        {DAY: ['01.01.2018', '02.01.2018', '04.05.2018', '15.05.2018', '04.02.2019', '18.06.2019', '20.06.2019',
               '20.06.2019',
               '20.06.2019'],
         AMOUNT: [100, 200, 300.5, -100, 10.75, -5, 10, -220, -30.0],
         PAYER: ["VW", "Titi", "VW", "Supermarkt", "VW", "travel", "VW", "travel",
                 "Supermarkt"]
         })


def test_sum_all_by_month(transactions):
    result = {AMOUNT: [300.0, 200.5, 10.75, -245],
              'years': [2018, 2018, 2019, 2019],
              'months': [1, 5, 2, 6]}

    assert result == sut.TransactionsAnalyser("all", step="monthly").sum(transactions).to_dict('list')


def test_sum_by_month_grouped(transactions):
    result = {'Beguenstigter/Zahlungspflichtiger': ['Titi',
                                                    'VW',
                                                    'Supermarkt',
                                                    'VW',
                                                    'VW',
                                                    'Supermarkt',
                                                    'VW',
                                                    'travel'],
              'Betrag': [200.0, 100.0, -100.0, 300.5, 10.75, -30.0, 10.0, -225.0],
              'month': [1, 1, 5, 5, 2, 6, 6, 6],
              'years': [2018, 2018, 2018, 2018, 2019, 2019, 2019, 2019]}

    assert result == sut.TransactionsAnalyser("all", step="monthly", is_grouped=True).sum(
        transactions).to_dict('list')


def test_sum_all_the_transactions_over_the_year(transactions):
    result = {'Betrag': [500.5, -234.25], 'years': [2018, 2019]}

    assert result == sut.TransactionsAnalyser("all").sum(transactions).to_dict('list')


def test_retrieve_all_the_revenues_by_year_and_give_the_total(transactions):
    result = {'Buchungstag': [2018, 2018, 2019],
              'Beguenstigter/Zahlungspflichtiger': ['Titi', 'VW', 'VW'],
              'Betrag': [200.0, 400.5, 20.75]}
    assert result == sut.TransactionsAnalyser("revenues", is_grouped=True).sum(transactions).to_dict('list')


def test_get_the_revenues_for_each_year(transactions):
    result = {'years': [2018, 2019],
              'Betrag': [600.5, 20.75]}
    assert result == sut.TransactionsAnalyser("revenues").sum(transactions).to_dict('list')


def test_retrieve_all_the_expenses_by_year(transactions):
    result = {'Buchungstag': [2018, 2019, 2019],
              'Beguenstigter/Zahlungspflichtiger': ['Supermarkt', 'Supermarkt', 'travel'],
              'Betrag': [-100.0, -30.0, -225.0]}
    assert result == sut.TransactionsAnalyser("expenses", is_grouped=True).sum(transactions).to_dict('list')


def test_get_the_expenses_for_each_year(transactions):
    result = {'years': [2018, 2019],
              'Betrag': [-100, -255]}
    assert result == sut.TransactionsAnalyser("expenses").sum(transactions).to_dict('list')


def test_selections_of_groups(transactions):
    selections = ["VW", "Supermarkt"]

    usecase = sut.TransactionsAnalyser("all", is_grouped=True, selections=selections)
    result = usecase.sum(transactions)
    assert set(result[PAYER].values).issubset(selections)
    assert len(result) > 0


def test_categorize(transactions):
    transactions[PAYER] = ["VW", "Titi", "VW", "supermarkt", "", "travel", "VW", "travel",
                           "Supermarkt"]

    categories = {"salary": ["vw"], "food": ["supermarkt"]}
    categorized_data = sut.categorize(transactions, categories)

    assert categorized_data["category"].tolist() == ["salary", "other", "salary", "food", "other", "other", "salary",
                                                     "other", "food"]


@given(
    transaction_type=st.sampled_from(
        ["all", "revenues", "expenses", "saf", None, 8756]
    ),
    step=st.sampled_from(
        ["yearly", "monthly", "asfasfsaf", None]
    ),
    is_grouped=st.sampled_from(
        [True, False, "", 4568, "asdasd"]
    ),
    selections=st.sampled_from([random.sample(
        ["VW", "Titi", "VW Germ", "Supermarkt", "VW", "travel", "VW", "travel",
         "Supermarkt", None, 458], 3)]),
)
def test_with_hypotesis(transaction_type, step, is_grouped, selections):
    transactions = pd.DataFrame(
        {DAY: ['01.01.2018', '02.01.2018', '04.05.2018', '15.05.2018', '04.02.2019', '18.06.2019', '20.06.2019',
               '20.06.2019',
               '20.06.2019'],
         AMOUNT: [100, 200, 300.5, -100, 10.75, -5, 10, -220, -30.0],
         PAYER: ["VW", "Titi", "VW", "Supermarkt", "VW", "travel", "VW", "travel",
                 "Supermarkt"]
         })
    try:
        request = AnalyseRequest(transaction_type, step, is_grouped, selections)
        AnalyseRequestValidator().validate(request)
        usecase = sut.TransactionsAnalyser(transaction_type, step, is_grouped, selections).sum(transactions)
    except AgumentsErrors:
        pass
    except sut.NotDefinedTransactionTypeError:
        pass
