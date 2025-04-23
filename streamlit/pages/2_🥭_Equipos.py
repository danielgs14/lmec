import streamlit as st
import pandas as pd

from helpers.sheets_handler import read_player_data, write_team_data

st.set_page_config(
    page_title="Equipos",
    page_icon=":mango:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Google Sheet names
player_sheet_name = "player_data"
match_teams_sheet_name = "match_teams"

st.title("Equipos")

# Load player names from Google Sheets
player_data = read_player_data(player_sheet_name)
player_df = pd.DataFrame(player_data)

if player_df.empty:
    st.warning("No hay jugadores. Añádalos en 🥝 **Jugadores**")
    st.stop()

player_names = player_df["Nombre"].tolist()

# Select players for each team
team1 = st.multiselect("Equipo 1", player_names, max_selections=6)
team2 = st.multiselect(
    "Equipo 2",
    [p for p in player_names if p not in team1],  # Exclude already selected
    max_selections=6
)

if len(team1) != 6 or len(team2) != 6:
    st.info("Escoja seis jugadores por equipo.")
else:
    if st.button("Guardar equipos."):
        match_df = pd.DataFrame({
            "Nombre": team1 + team2,
            "Equipo": ["Equipo 1"] * 6 + ["Equipo 2"] * 6
        })
        write_team_data(match_teams_sheet_name, match_df.to_dict(orient="records"))
        st.success("Equipos guardados para la mejenga.")
