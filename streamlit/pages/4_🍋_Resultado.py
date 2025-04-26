import streamlit as st
import pandas as pd
from helpers.sheets_handler import (
    read_player_data, write_player_data, 
    read_team_data, read_goals_data, append_snapshot_data
)

st.set_page_config(
    page_title="Resultados",
    page_icon=":lemon:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# sheets
player_sheet = "player_data"
team_sheet = "match_teams"
goals_sheet = "personal_goals"
snapshot_sheet = "snapshot_data"

team_df = pd.DataFrame(read_team_data(team_sheet))
goal_df = pd.DataFrame(read_goals_data(goals_sheet))
player_df = pd.DataFrame(read_player_data(player_sheet))

# st stuff
st.title("Resultados")

if team_df.empty:
    st.warning("No ha escogido equipos. Por favor regrese a 🥭 **Equipos**.")
    st.stop()

if goal_df.empty:
    st.warning("Sin goles individuales. Use 🍌 **Goles**.")
    st.stop()

team_names = team_df["Equipo"].unique()
if len(team_names) != 2:
    st.error("Deben existir exactamente dos equipos para continuar.")
    st.stop()

team1_name, team2_name = team_names
team1_players = team_df[team_df["Equipo"] == team1_name]["Nombre"].tolist()
team2_players = team_df[team_df["Equipo"] == team2_name]["Nombre"].tolist()

st.subheader("Resultados de la mejenga")
col1, col2 = st.columns(2)
with col1:
    score_team1 = st.number_input(f"{team1_name}", min_value=0, step=1, key="score1")
with col2:
    score_team2 = st.number_input(f"{team2_name}", min_value=0, step=1, key="score2")


if st.button("Ingresar marcador"):
    result_team1, result_team2 = (
        ("draw", "draw") if score_team1 == score_team2 else
        ("win", "loss") if score_team1 > score_team2 else
        ("loss", "win")
    )

    for team_players, opponent_players, result, team_score, opponent_score in zip(
        [team1_players, team2_players],
        [team2_players, team1_players],
        [result_team1, result_team2],
        [score_team1, score_team2],
        [score_team2, score_team1]
    ):
        for player in team_players:
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

    write_player_data(player_sheet, player_df.to_dict(orient="records"))

    snapshot_df = pd.merge(player_df, team_df[["Nombre", "Equipo"]], on="Nombre", how="left")
    snapshot_df["partido"] = pd.to_datetime("today").strftime("%Y-%m-%d, %H:%M")
    snapshot_df = snapshot_df.replace([float("inf"), float("-inf")], 0)
    snapshot_df = snapshot_df.fillna("Sin Jugar")

    append_snapshot_data(snapshot_sheet, snapshot_df.to_dict(orient="records"))



    st.session_state.goal_counts = {player: 0 for player in player_df["Nombre"].tolist()}

    st.success("Se guardaron los resultados y estadísticas de jugadores.")
