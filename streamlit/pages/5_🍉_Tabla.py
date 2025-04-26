import streamlit as st
import pandas as pd
from helpers.sheets_handler import read_player_data, read_snapshot_data

st.set_page_config(
    page_title="Stats",
    page_icon=":watermelon:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# sheets
player_sheet_name = "player_data"
snapshot_sheet_name = "snapshot_data"

# st stuff
st.title("🏆Tabla General")
st.subheader("Tabla")
st.markdown("Esperar un minuto luego de ingresar resultados y refrescar.")


snapshot_df = pd.DataFrame(read_snapshot_data(snapshot_sheet_name))
snapshot_df["partido"] = pd.to_datetime(snapshot_df["partido"], errors="coerce")

snapshot_df = snapshot_df.sort_values(by=["Nombre", "partido"])
snapshot_df["delta_puntos"] = snapshot_df.groupby("Nombre")["Puntos"].diff()
latest_date = snapshot_df["partido"].max()
latest_snapshot = snapshot_df[snapshot_df["partido"] == latest_date].copy()

def points_arrows(row):
    if pd.isna(row["delta_puntos"]):
        return row["Puntos"]
    elif row["delta_puntos"] > 0:
        return f'{row["Puntos"]} ⬆️'
    elif row["delta_puntos"] < 0:
        return f'{row["Puntos"]} ⬇️'
    else:
        return f'{row["Puntos"]} ↔️'

latest_snapshot["Puntos"] = latest_snapshot.apply(points_arrows, axis=1)
latest_snapshot = latest_snapshot.sort_values(by=["Puntos", "PG", "GInd", "GF"], ascending=False).reset_index(drop=True)

medals = ["🥇", "🥈", "🥉"]
for i in range(min(3, len(latest_snapshot))):
    latest_snapshot.at[i, "Nombre"] = f"{medals[i]} {latest_snapshot.at[i, 'Nombre']}"

st.dataframe(
    latest_snapshot.sort_values(by=["Puntos", "PG", "GInd", "GF"], ascending=False).drop(columns=["delta_puntos", "partido", "Equipo"]),
    hide_index=True
)
