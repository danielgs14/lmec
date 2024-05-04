import streamlit as st

# Player dictionary/list
player_data = {
  "player_1": {"points": 0, "games_played": 0, "games_won": 0, "games_drawn": 0, "games_lost": 0, "goals_for": 0, "goals_against": 0},
  "player_2": {"points": 0, "games_played": 0, "games_won": 0, "games_drawn": 0, "games_lost": 0, "goals_for": 0, "goals_against": 0},
  "player_3": {"points": 0, "games_played": 0, "games_won": 0, "games_drawn": 0, "games_lost": 0, "goals_for": 0, "goals_against": 0},
  "player_4": {"points": 0, "games_played": 0, "games_won": 0, "games_drawn": 0, "games_lost": 0, "goals_for": 0, "goals_against": 0},
  "player_5": {"points": 0, "games_played": 0, "games_won": 0, "games_drawn": 0, "games_lost": 0, "goals_for": 0, "goals_against": 0},
  "player_6": {"points": 0, "games_played": 0, "games_won": 0, "games_drawn": 0, "games_lost": 0, "goals_for": 0, "goals_against": 0},
  "player_7": {"points": 0, "games_played": 0, "games_won": 0, "games_drawn": 0, "games_lost": 0, "goals_for": 0, "goals_against": 0},
  "player_8": {"points": 0, "games_played": 0, "games_won": 0, "games_drawn": 0, "games_lost": 0, "goals_for": 0, "goals_against": 0},
  "player_9": {"points": 0, "games_played": 0, "games_won": 0, "games_drawn": 0, "games_lost": 0, "goals_for": 0, "goals_against": 0},
  "player_10": {"points": 0, "games_played": 0, "games_won": 0, "games_drawn": 0, "games_lost": 0, "goals_for": 0, "goals_against": 0},
  "player_11": {"points": 0, "games_played": 0, "games_won": 0, "games_drawn": 0, "games_lost": 0, "goals_for": 0, "goals_against": 0},
  "player_12": {"points": 0, "games_played": 0, "games_won": 0, "games_drawn": 0, "games_lost": 0, "goals_for": 0, "goals_against": 0},
  "player_13": {"points": 0, "games_played": 0, "games_won": 0, "games_drawn": 0, "games_lost": 0, "goals_for": 0, "goals_against": 0},
  "player_14": {"points": 0, "games_played": 0, "games_won": 0, "games_drawn": 0, "games_lost": 0, "goals_for": 0, "goals_against": 0},
}

# Function to update player data
def updater(team_a, team_b, score_a, score_b):
   # Calculate winner and points
  score_diff = score_a - score_b

  if score_diff == 0:
    winner = "Empate"
    winner_points = 1
    loser_points = 1
  else:
    winner = "Team A" if score_a > score_b else "Team B"
    winner_points = 3 if winner != "Empate" else 1
    loser_points = 0 if winner != "Empate" else 1

# Update data for each player in winning and losing teams
  for player in team_a:
    player_data[player]["points"] += winner_points
    player_data[player]["games_played"] += 1  
    player_data[player]["games_won"] += 1 if winner == "Team A" else 0
    player_data[player]["games_drawn"] += 1 if winner == "Draw" else 0
    player_data[player]["games_lost"] += 1 if winner == "Team B" else 0
    player_data[player]["goals_for"] += score_a
    player_data[player]["goals_against"] += score_b
  for player in team_b:
    player_data[player]["points"] += loser_points
    player_data[player]["games_played"] += 1  
    player_data[player]["games_won"] += 1 if winner == "Team B" else 0
    player_data[player]["games_drawn"] += 1 if winner == "Draw" else 0
    player_data[player]["games_lost"] += 1 if winner == "Team A" else 0
    player_data[player]["goals_for"] += score_a
    player_data[player]["goals_against"] += score_b

# Streamlit interface
team_a = st.multiselect("Select Team A Players", list(player_data.keys()), 6)
team_b = st.multiselect("Select Team B Players", list(player_data.keys()), 6)
score_a = st.number_input("Team A Score", min_value=0)
score_b = st.number_input("Team B Score", min_value=0)

if st.button("Update Table"):
  updater(team_a, team_b, score_a, score_b)

# Display updated player data table
st.dataframe(player_data)