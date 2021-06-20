import pytest
import pandas as pd
from cashflow_analyzer import usecase


def no_errors(uc):
    return len(uc.errors) == 0


def test_errors_if_the_information_does_not_have_the_right_name():
    transactions = pd.DataFrame({"datum": [],
                                 "values": []})
    uc = usecase.CalculateCashflow(transactions)
    assert no_errors(uc)
    uc.execute()
    assert uc.errors == {"wrong_columns_information": ["datum",
                                                       "values"]}


def test_no_errors_if_the_columns_name_are_conform():
    transactions = pd.DataFrame({"dates": [],
                                 "amounts": []})
    uc = usecase.CalculateCashflow(transactions)
    uc.execute()
    assert no_errors(uc)


def test_errors_wrong_data_type_as_input():
    transactions = list()
    uc = usecase.CalculateCashflow(transactions)
    uc.execute()

    assert uc.errors["wrong_type_input"] == [f'transaction is {type(transactions)} '
                                             f'instead of dataframe']


def test_throw_exception_if_illegal_arguments():
    transactions = pd.DataFrame({"datum": ["01.01.2019", "03.01.2019"],
                                 "values": [100, -150]})
    uc = usecase.CalculateCashflow(transactions)
    with pytest.raises(ValueError) as e:
        uc.execute()


def test_calculate_cashflow_for_one_month():
    transactions = pd.DataFrame({"datum": ["01.01.2019", "03.01.2019"],
                                 "values": [100, -150]})
    uc = usecase.CalculateCashflow(transactions)
    assert uc.cashflow == 0
    uc.execute()
    assert uc.cashflow == transactions["values"].sum()
