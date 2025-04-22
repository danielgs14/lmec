import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Equipos",
    page_icon=":mango:",
    layout="wide",
    initial_sidebar_state="expanded"
)
# filepaths
player_filepath = "./tables/player_data.csv"
team_filepath = "./tables/match_teams.csv"

st.title("Equipos")

# Load player names
if not os.path.exists(player_filepath):
    st.warning("No hay jugadores. Añádalos en 🥝 **Jugadores**")
    st.stop()

player_df = pd.read_csv(player_filepath)
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
        match_df.to_csv(team_filepath, index=False)
        st.success("Equipos guardados para la mejenga.")
