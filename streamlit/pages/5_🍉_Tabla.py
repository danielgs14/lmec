import streamlit as st
import pandas as pd
from helpers.sheets_handler import read_player_data

st.set_page_config(
    page_title="Stats",
    page_icon=":watermelon:",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Tabla General")

# sheets stuff
player_sheet_name = "player_data"
# snapshot_sheet_name = "player_snapshots" 

# st stuff
st.subheader("Tabla")

player_data = read_player_data(player_sheet_name)
player_df = pd.DataFrame(player_data)

if player_df.empty:
    st.info("No hay datos disponibles.")
else:
    player_df = player_df.sort_values(by=["Puntos", "PG", "GInd", "GF"], ascending=False).reset_index(drop=True)
    st.dataframe(player_df, hide_index=True, use_container_width=True)
