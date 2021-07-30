import pytest

from cashflow_analyzer.requests import AnalyseRequest, AgumentsErrors, AnalyseRequestValidator
from cashflow_analyzer.transactions import TRANSACTIONS_TYPES, STEP_TYPES

POSSIBLE_TYPES = list(TRANSACTIONS_TYPES.keys())
POSSIBLE_STEPS = list(STEP_TYPES)


@pytest.fixture(name="validator")
def fixture_analyse_request_validator():
    return AnalyseRequestValidator()


def test_input_validation_type(validator):
    try:
        validator.validate(AnalyseRequest(type="all", step="monthly", grouped=True))
    except AgumentsErrors():
        assert 0 == len(validator.errors)


def test_validate_input_type(validator):
    try:
        arg = 54
        validator.validate(AnalyseRequest(type=arg))
    except AgumentsErrors:
        assert f"{arg} not in {POSSIBLE_TYPES}" == validator.errors[0]


def test_validate_type(validator):
    try:
        arg = "not a boolean"
        validator.validate(AnalyseRequest(grouped=arg))
    except AgumentsErrors:
        assert f"{arg} is not <class 'bool'>" == validator.errors[0]


def test_many_mistake(validator):
    try:
        validator.validate(
            AnalyseRequest(type=None,
                           step=56,
                           grouped=58.5,
                           payers={"tada": 5})
        )
    except AgumentsErrors:
        assert 4 == len(validator.errors)
