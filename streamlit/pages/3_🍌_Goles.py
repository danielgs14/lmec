import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Goles",
    page_icon=":banana:",
    layout="wide",
    initial_sidebar_state="expanded"
)

team_filepath = "./tables/match_teams.csv"
goals_filepath = "./tables/personal_goals.csv"

st.title("Goles")

# Check if team file exists
if not os.path.exists(team_filepath):
    st.warning("No ha escogido los equipos. Regrese a 🥭 Equipos para seleccionarlos.")
    st.stop()

# Load team data
team_df = pd.read_csv(team_filepath)
players = team_df["Nombre"].tolist()

# Reset goal counts if players changed
if "goal_counts" not in st.session_state or set(st.session_state.goal_counts.keys()) != set(players):
    st.session_state.goal_counts = {player: 0 for player in players}

# Reset all goals button
if st.button("Resetear goles"):
    for player in players:
        st.session_state.goal_counts[player] = 0
    st.success("Goles reseteados.")

st.subheader("Presione cada nombre para añadir un gol.")

# Display goal buttons
for team in team_df["Equipo"].unique():
    st.markdown(f"### {team}")
    team_players = team_df[team_df["Equipo"] == team]["Nombre"].tolist()
    cols = st.columns(6)

    for i, player in enumerate(team_players):
        with cols[i % 6]:
            if st.button(f"{player}", key=f"btn_{player}"):
                st.session_state.goal_counts[player] += 1
            st.write(f"Goles: {st.session_state.goal_counts[player]}")

# Show total goals per team
team1_goals = sum(
    st.session_state.goal_counts.get(player, 0)
    for player in team_df[team_df["Equipo"] == "Equipo 1"]["Nombre"]
)
team2_goals = sum(
    st.session_state.goal_counts.get(player, 0)
    for player in team_df[team_df["Equipo"] == "Equipo 2"]["Nombre"]
)

st.markdown("### Goles por Equipo")
col1, col2 = st.columns(2)
col1.metric("Equipo 1", f"{team1_goals} goles")
col2.metric("Equipo 2", f"{team2_goals} goles")

# Save to file
if st.button("Guardar Goles Individuales"):
    goal_df = pd.DataFrame([
        {"Nombre": player, "GInd": goals}
        for player, goals in st.session_state.goal_counts.items()
    ])
    goal_df.to_csv(goals_filepath, index=False)
    st.success("Goles personales guardados.")
