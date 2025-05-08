import gspread
import pandas as pd
import streamlit as st
from google.oauth2.service_account import Credentials


# filepaths
scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scopes)

client = gspread.authorize(creds)

def get_sheet(sheet_name="Your Sheet Name"):
    sheet = client.open(sheet_name).sheet1
    return sheet

@st.cache_data(ttl=60)
def read_player_data(sheet_name):
    sheet = client.open(sheet_name).sheet1
    records = sheet.get_all_records()
    
    if not records:
        headers = ["Nombre", "PJ", "PG", "PE", "PP", "GF", "GC", "GInd", "Puntos"]
        sheet.append_row(headers)
        return pd.DataFrame(columns=headers)
    
    return pd.DataFrame(records)


def write_player_data(sheet_name, data, append=False):
    if data is None or not data:
        raise ValueError("No data to write.")
    
    sheet = get_sheet(sheet_name)
    headers = ["Nombre", "PJ", "PG", "PE", "PP", "GF", "GC", "GInd", "Puntos"]

    if append:
        record = data[0]  # not data[-1]
        cleaned_row = []
        for value in record.values():
            if pd.isna(value) or value in [float("inf"), -float("inf")]:
                cleaned_row.append("")
            else:
                cleaned_row.append(value)
        sheet.append_row(cleaned_row)
    else:
        sheet.clear()
        sheet.append_row(headers)

        cleaned_data = []
        for record in data:
            cleaned_record = []
            for value in record.values():
                if pd.isna(value) or value in [float("inf"), -float("inf")]:
                    cleaned_record.append("")
                else:
                    cleaned_record.append(value)
            cleaned_data.append(cleaned_record)

        for row in cleaned_data:
            sheet.append_row(row)


@st.cache_data(ttl=60)
def read_team_data(sheet_name):
    sheet = get_sheet(sheet_name)
    data = sheet.get_all_records()

    if not data:
        sheet.append_row(["Nombre", "Equipo"])
        return []

    return data

def write_team_data(sheet_name, data):
    if data is None:
        raise ValueError("No data to write.")
    
    sheet = get_sheet(sheet_name)
    sheet.clear()
    sheet.append_row(["Nombre", "Equipo"])
    for row in data:
        sheet.append_row([row["Nombre"], row["Equipo"]])

@st.cache_data(ttl=60)
def read_goals_data(sheet_name):
    sheet = get_sheet(sheet_name)
    data = sheet.get_all_records()
    
    if not data:
        sheet.append_row(["Nombre", "GInd"])
        return []

    return data


def write_goals_data(sheet_name, data):
    if data is None:
        raise ValueError("No data to write.")
    
    sheet = get_sheet(sheet_name)
    sheet.clear()
    
    # Now includes "Equipo"
    sheet.append_row(["Nombre", "Equipo", "GInd"])
    
    for record in data:
        row = [
            record.get("Nombre", ""),
            record.get("Equipo", ""),  # New: Team name
            record.get("GInd", 0)
        ]
        sheet.append_row(row)


@st.cache_data(ttl=60)
def read_snapshot_data(sheet_name):
    worksheet = get_sheet(sheet_name)
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    return df

def append_snapshot_data(sheet_name, data):
    sheet = get_sheet(sheet_name)
    existing = sheet.get_all_records()
    if not existing:
        sheet.append_row(list(data[0].keys()))
    for row in data:
        sheet.append_row(list(row.values()))
