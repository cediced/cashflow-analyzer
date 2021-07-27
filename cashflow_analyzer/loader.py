import pandas as pd

from cashflow_analyzer.transactions import SCHEMA


def get_data(path_data):
    return pd.read_csv(path_data, sep=";")


def convert(data: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame()
    df[SCHEMA["day"]] = data["Booking date"].str.replace("/", ".")
    df[SCHEMA["amount"]] = data["Credit"].fillna(0) + data["Debit"].fillna(0)
    df[SCHEMA["payer"]] = data["Beneficiary / Originator"].fillna("") + data["Payment Details"].fillna("")
    return df
