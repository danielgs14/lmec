import streamlit as st
import pandas as pd

from helpers.sheets_handler import read_player_data, write_team_data

st.set_page_config(
    page_title="Equipos",
    page_icon=":mango:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# sheets stuff
player_sheet_name = "player_data"
match_teams_sheet_name = "match_teams"

player_data = read_player_data(player_sheet_name)
player_df = pd.DataFrame(player_data)


# st stuff
st.title("Equipos")

if player_df.empty:
    st.warning("No hay jugadores. Añádalos en 🥝 **Jugadores**")
    st.stop()

player_names = player_df["Nombre"].tolist()

team1_name = st.text_input("Nombre para Equipo 1", value="Equipo 1")
team2_name = st.text_input("Nombre para Equipo 2", value="Equipo 2")


team1 = st.multiselect("Equipo 1", player_names, max_selections=6)
team2 = st.multiselect(
    "Equipo 2",
    [p for p in player_names if p not in team1], 
    max_selections=6
)

if len(team1) != 6 or len(team2) != 6:
    st.info("Escoja seis jugadores por equipo.")
else:
    if st.button("Guardar equipos."):
        match_df = pd.DataFrame({
            "Nombre": team1 + team2,
            "Equipo": [team1_name] * 6 + [team2_name] * 6
        })
        write_team_data(match_teams_sheet_name, match_df.to_dict(orient="records"))
        st.success("Equipos guardados para la mejenga.")
