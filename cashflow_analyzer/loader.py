import pandas as pd

from cashflow_analyzer.transactions import SCHEMA


def get_data(path_data):
    return pd.read_csv(path_data, sep=";")


def db_convertor(data: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame()
    df[SCHEMA["day"]] = data["Booking date"].str.replace("/", ".")
    df[SCHEMA["day"]] = pd.to_datetime(data["Booking date"].str.replace("/", "."), format='%m.%d.%Y')
    df[SCHEMA["day"]] = df[SCHEMA["day"]].dt.strftime('%d.%m.%Y')

    df[SCHEMA["amount"]] = data["Credit"].str.replace(",", "").fillna(0).astype("float") + data["Debit"].str.replace(
        ",", "").fillna(0).astype("float")
    df[SCHEMA["payer"]] = data["Beneficiary / Originator"].fillna("") + data["Payment Details"].fillna("")
    return df


def sparkasse_convertor(data: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame()
    df[SCHEMA["day"]] = data["Buchungstag"].str.replace("/", ".")
    df[SCHEMA["day"]] = pd.to_datetime(data["Buchungstag"].str.replace("/", "."), format='%d.%m.%y')
    df[SCHEMA["day"]] = df[SCHEMA["day"]].dt.strftime('%d.%m.%Y')

    df[SCHEMA["amount"]] = data["Betrag"].str.replace(",", ".").astype(float)
    df[SCHEMA["payer"]] = data["Beguenstigter/Zahlungspflichtiger"]
    df[SCHEMA["payer"]] = df[SCHEMA["payer"]].fillna("custom_nan")
    return df
