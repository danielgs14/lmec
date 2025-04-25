import streamlit as st
import pandas as pd
from helpers.sheets_handler import read_player_data, read_snapshot_data

st.set_page_config(
    page_title="Stats",
    page_icon=":watermelon:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# sheets stuff
player_sheet_name = "player_data"
snapshot_sheet_name = "snapshot_data" 

# st stuff
st.title("🏆Tabla General")

st.subheader("Tabla")
st.markdown("Esperar un minuto luego de ingresar resultados y refrescar.")

player_data = read_player_data(player_sheet_name)
player_df = pd.DataFrame(player_data)
snapshot_df = read_snapshot_data(snapshot_sheet_name) 


if player_df.empty:
    st.info("No hay datos disponibles.")
else:
    player_df = player_df.sort_values(by=["Puntos", "PG", "GInd", "GF"], ascending=False).reset_index(drop=True)
    st.dataframe(player_df, hide_index=True, use_container_width=True)


snapshot_df = snapshot_df.sort_values(by=["Nombre", "Fecha"])
snapshot_df["delta_puntos"] = snapshot_df.groupby("Nombre")["Puntos"].diff()
latest_date = snapshot_df["Fecha"].max()

latest_snapshot = snapshot_df[snapshot_df["Fecha"] == latest_date].copy()

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