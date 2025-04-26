import streamlit as st
import pandas as pd

from helpers.sheets_handler import read_team_data, write_goals_data

st.set_page_config(
    page_title="Goles",
    page_icon=":banana:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# sheets stuff
match_teams_sheet = "match_teams"
personal_goals_sheet = "personal_goals"

team_data = read_team_data(match_teams_sheet)
team_df = pd.DataFrame(team_data)

# st stuff
st.title("Goles")

if team_df.empty:
    st.warning("No ha escogido los equipos. Regrese a 🥭 Equipos para seleccionarlos.")
    st.stop()

players = team_df["Nombre"].tolist()

# Initialize goal counts
if "goal_counts" not in st.session_state or set(st.session_state.goal_counts.keys()) != set(players):
    st.session_state.goal_counts = {player: 0 for player in players}

if st.button("Resetear goles"):
    for player in players:
        st.session_state.goal_counts[player] = 0
    st.success("Goles reseteados.")

st.subheader("Presione cada nombre para añadir un gol.")

team_names = team_df["Equipo"].unique()

for team in team_names:
    st.markdown(f"### {team}")
    team_players = team_df[team_df["Equipo"] == team]["Nombre"].tolist()
    cols = st.columns(6)

    for i, player in enumerate(team_players):
        with cols[i % 6]:
            if st.button(f"{player}", key=f"btn_{player}"):
                st.session_state.goal_counts[player] += 1
            st.write(f"Goles: {st.session_state.goal_counts[player]}")

# Dynamic team goal summaries
st.markdown("### Goles por Equipo")
cols = st.columns(len(team_names))

for i, team in enumerate(team_names):
    total_goals = sum(
        st.session_state.goal_counts.get(player, 0)
        for player in team_df[team_df["Equipo"] == team]["Nombre"]
    )
    cols[i].metric(team, f"{total_goals} goles")

if st.button("Guardar Goles Individuales"):
    goal_df = pd.DataFrame([
        {
            "Nombre": player,
            "Equipo": team_df[team_df["Nombre"] == player]["Equipo"].values[0],
            "GInd": goals
        }
        for player, goals in st.session_state.goal_counts.items()
    ])
    write_goals_data(personal_goals_sheet, goal_df.to_dict(orient="records"))
    st.success("Goles personales guardados.")
