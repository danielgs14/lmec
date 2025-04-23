import streamlit as st
import pandas as pd
from helpers.sheets_handler import read_player_data, write_player_data,read_team_data, read_goals_data,append_snapshot_data

st.set_page_config(
    page_title="Resultados",
    page_icon=":lemon:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sheet names
player_sheet = "player_data"
team_sheet = "match_teams"
goals_sheet = "personal_goals"
snapshot_sheet = "snapshot_data"

st.title("Resultados")

# Load data from Google Sheets
team_df = pd.DataFrame(read_team_data(team_sheet))
goal_df = pd.DataFrame(read_goals_data(goals_sheet))
player_df = pd.DataFrame(read_player_data(player_sheet))

if team_df.empty:
    st.warning("No ha escogido equipos. Por favor regrese a 🥭 **Equipos**.")
    st.stop()

if goal_df.empty:
    st.warning("Sin goles individuales. Use 🍌 **Goles**.")
    st.stop()

# Get teams
team1 = team_df[team_df["Equipo"] == "Equipo 1"]["Nombre"].tolist()
team2 = team_df[team_df["Equipo"] == "Equipo 2"]["Nombre"].tolist()

# Input final score
st.subheader("Resultados de la mejenga")
score_team1 = st.number_input("Resultado del equipo 1", min_value=0, step=1)
score_team2 = st.number_input("Resultado del equipo 2", min_value=0, step=1)

if st.button("Ingresar marcador"):
    result_team1, result_team2 = (
        ("draw", "draw") if score_team1 == score_team2 else
        ("win", "loss") if score_team1 > score_team2 else
        ("loss", "win")
    )

    for team, opponent_team, result, team_score, opponent_score in zip(
        [team1, team2], [team2, team1], [result_team1, result_team2], [score_team1, score_team2], [score_team2, score_team1]
    ):
        for player in team:
            player_df.loc[player_df["Nombre"] == player, "PJ"] += 1
            player_df.loc[player_df["Nombre"] == player, "GF"] += team_score
            player_df.loc[player_df["Nombre"] == player, "GC"] += opponent_score

            personal_goals = goal_df[goal_df["Nombre"] == player]["GInd"].sum()
            player_df.loc[player_df["Nombre"] == player, "GInd"] += personal_goals

            if result == "win":
                player_df.loc[player_df["Nombre"] == player, "PG"] += 1
                player_df.loc[player_df["Nombre"] == player, "Puntos"] += 3
            elif result == "draw":
                player_df.loc[player_df["Nombre"] == player, "PE"] += 1
                player_df.loc[player_df["Nombre"] == player, "Puntos"] += 1
            else:
                player_df.loc[player_df["Nombre"] == player, "PP"] += 1

    # Write updated data
    write_player_data(player_sheet, player_df.to_dict(orient="records"))

    # Append snapshot with date
    snapshot_df = player_df.copy()
    snapshot_df["partido"] = pd.to_datetime("today").strftime("%Y-%m-%d")
    append_snapshot_data(snapshot_sheet, snapshot_df.to_dict(orient="records"))

    st.session_state.goal_counts = {player: 0 for player in player_df["Nombre"].tolist()}

    st.success("Se guardaron los resultados y estadísticas de jugadores.")
