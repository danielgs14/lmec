import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Resultados",
    page_icon=":lemon:",
    layout="wide",
    initial_sidebar_state="expanded"
)

player_filepath = "./tables/player_data.csv"
team_filepath = "./tables/match_teams.csv"
goals_filepath = "./tables/personal_goals.csv"
snapshot_filepath = "./tables/player_snapshots.csv"

st.title("Resultados")

# Check required files exist
if not os.path.exists(team_filepath):
    st.warning("No ha escogido equipos. Por favor regrese a 🥭 **Equipos**.")
    st.stop()

if not os.path.exists(goals_filepath):
    st.warning("Sin goles individuales. Use 🍌 **Goles**.")
    st.stop()

# Load data
team_df = pd.read_csv(team_filepath)
goal_df = pd.read_csv(goals_filepath)
player_df = pd.read_csv(player_filepath)

# Get teams
team1 = team_df[team_df["Equipo"] == "Equipo 1"]["Nombre"].tolist()
team2 = team_df[team_df["Equipo"] == "Equipo 2"]["Nombre"].tolist()

# Input final score
st.subheader("Resultados de la mejenga")
score_team1 = st.number_input("Resultado del equipo 1", min_value=0, step=1)
score_team2 = st.number_input("Resultado del equipo 2", min_value=0, step=1)

if st.button("Ingresar marcador"):
    # Determine results
    if score_team1 == score_team2:
        result_team1 = result_team2 = "draw"
    elif score_team1 > score_team2:
        result_team1 = "win"
        result_team2 = "loss"
    else:
        result_team1 = "loss"
        result_team2 = "win"

    # Update stats for each team
    for team, opponent_team, result, team_score, opponent_score in zip(
        [team1, team2], [team2, team1], [result_team1, result_team2], [score_team1, score_team2], [score_team2, score_team1]
    ):
        for player in team:
            player_df.loc[player_df["Nombre"] == player, "PJ"] += 1
            player_df.loc[player_df["Nombre"] == player, "GF"] += team_score
            player_df.loc[player_df["Nombre"] == player, "GC"] += opponent_score

            # Add personal goals
            personal_goals = goal_df[goal_df["Nombre"] == player]["GInd"].sum()
            player_df.loc[player_df["Nombre"] == player, "GInd"] += personal_goals

            # Update result-based stats
            if result == "win":
                player_df.loc[player_df["Nombre"] == player, "PG"] += 1
                player_df.loc[player_df["Nombre"] == player, "Puntos"] += 3
            elif result == "draw":
                player_df.loc[player_df["Nombre"] == player, "PE"] += 1
                player_df.loc[player_df["Nombre"] == player, "Puntos"] += 1
            else:
                player_df.loc[player_df["Nombre"] == player, "PP"] += 1

    # Save updated player data
    player_df.to_csv(player_filepath, index=False)

    # Save snapshot
    snapshot_df = player_df.copy()
    snapshot_df["partido"] = pd.to_datetime("today").strftime("%Y-%m-%d")
    snapshot_df.to_csv(snapshot_filepath, mode="a", header=not os.path.exists(snapshot_filepath), index=False)

    # Reset session state for goals
    st.session_state.goal_counts = {player: 0 for player in player_df["Nombre"].tolist()}

    st.success("Se guardaron los resultados y estadísticas de jugadores.")
