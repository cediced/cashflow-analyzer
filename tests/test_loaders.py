import pandas as pd
import numpy as np
import pytest

from cashflow_analyzer import loader
from cashflow_analyzer.transactions import SCHEMA, TransactionsAnalyser


DEUTSCHE_BANK_DF = pd.DataFrame(
        {
            "Booking date": ["01/27/2021", "06/30/2021"],
            "Beneficiary / Originator": ["EDEKA", None],
            "Payment Details": [None, "multiplus"],
            "Debit": [None, "-5.0"],
            "Credit": ["2,160.5", None],
            "dummy": [1,2]
        }
    )


SPARKASSE_DF = pd.DataFrame(
            {
                "Buchungstag": ["27.01.21", "30.06.21"],
                "Beguenstigter/Zahlungspflichtiger": ["EDEKA", "multiplus"],
                "Betrag": ["2160,5", "-5,0"],
                "dummy": [1,2]
            }
        )


@pytest.mark.parametrize("convertor, input_df",
                         [
                             (loader.db_convertor, DEUTSCHE_BANK_DF),
                             (loader.sparkasse_convertor, SPARKASSE_DF)
                         ])
def test_change_deutsche_bank_columns(convertor, input_df):

    df = convertor(input_df)
    expected = pd.DataFrame({

        SCHEMA["day"]: ["27.01.2021", "30.06.2021"],
        SCHEMA["amount"]: [2160.5, -5.0],
        SCHEMA["payer"]: ["EDEKA", "multiplus"]
    })
    assert expected.to_dict() == df.to_dict()
    assert TransactionsAnalyser("all", step="monthly").sum(df).to_dict('list') is not None
