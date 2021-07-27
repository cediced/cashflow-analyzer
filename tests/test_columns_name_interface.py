import pandas as pd
import numpy as np
from cashflow_analyzer import loader
from cashflow_analyzer.transactions import SCHEMA


def test_change_deutsche_bank_columns():
    data = pd.DataFrame(
        {
            "Booking date": ["01/27/2021", "02/27/2021"],
            "Beneficiary / Originator": ["EDEKA", None],
            "Payment Details": [None, "multiplus"],
            "Debit": [None, "-5.0"],
            "Credit": ["2,160.5", None]
        }
    )

    df = loader.convert(data)
    expected = pd.DataFrame({

        SCHEMA["day"]: ["01.27.2021", "02.27.2021"],
        SCHEMA["amount"]: [2160.5, -5.0],
        SCHEMA["payer"]: ["EDEKA", "multiplus"]
    })
    assert expected.to_dict() == df.to_dict()
