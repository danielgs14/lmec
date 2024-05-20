import streamlit as st
import pandas as pd

# Streamlit configuration
st.set_page_config(page_title="My App", page_icon="", layout="wide", initial_sidebar_state="collapsed")

# Define player data dictionary (replace with your data)
if 'player_data' not in st.session_state:
  st.session_state['player_data'] = {
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

player_data = st.session_state['player_data']

# Function to update player data
def update_data(team_a, team_b, score_a, score_b):
  # Calculate winner and points
  score_diff = score_a - score_b

  if score_diff == 0:
    # It's a draw! Assign 1 point to each player
    winner = "Draw"
    winner_points = 1
    loser_points = 1
  else:
    # Proceed with assigning points based on winner
    winner = "Team A" if score_a > score_b else "Team B"
    winner_points = 3 if winner != "Draw" else 1
    loser_points = 0 if winner != "Draw" else 1

  # Update data for each player in winning and losing teams
  for player in team_a:
    player_data[player]["points"] += winner_points if winner == "Team A" else (1 if winner == "Draw" else 0)
    player_data[player]["games_played"] += 1  
    player_data[player]["games_won"] += 1 if winner == "Team A" else 0
    player_data[player]["games_drawn"] += 1 if winner == "Draw" else 0
    player_data[player]["games_lost"] += 1 if winner == "Team B" else 0
    player_data[player]["goals_for"] += score_a
    player_data[player]["goals_against"] += score_b
  for player in team_b:
    player_data[player]["points"] += winner_points if winner == "Team B" else (1 if winner == "Draw" else 0)
    player_data[player]["games_played"] += 1  
    player_data[player]["games_won"] += 1 if winner == "Team B" else 0
    player_data[player]["games_drawn"] += 1 if winner == "Draw" else 0
    player_data[player]["games_lost"] += 1 if winner == "Team A" else 0
    player_data[player]["goals_for"] += score_b
    player_data[player]["goals_against"] += score_a


def load_data():
  """Loads player data from a CSV file (if it exists)."""
  global player_data  # Declare player_data as global

  try:
    df = pd.read_csv("player_data.csv")
    if isinstance(player_data, list):  # Check if player_data is a list (assuming it's initially a list)
      player_data.clear()  # Clear the list if empty
    player_data = df.to_dict(orient='records')
    st.success("Player data loaded successfully!")
  except FileNotFoundError:
    st.warning("No player data file found. Using initial data.")
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


def save_data():
#  Saves player data to a CSV file
  df = pd.DataFrame.from_dict(player_data, orient='index')
  df.to_csv("player_data.csv", index=True)
  print("Player data saved successfully!")

# Streamlit interface
if st.button("Load Player Data"):
  load_data()

available_players = player_data.keys()  # Get all player names initially
team_a = st.multiselect("Select Team A Players", available_players)
# Filter available players for Team B based on selections in Team A
filtered_players = [player for player in available_players if player not in team_a]
team_b = st.multiselect("Select Team B Players", filtered_players)

# team_a = st.multiselect("Select Team A Players", player_data.keys())
# team_b = st.multiselect("Select Team B Players", player_data.keys())
score_a = st.number_input("Team A Score", min_value=0)
score_b = st.number_input("Team B Score", min_value=0)

if st.button("Update Table"):
  update_data(team_a, team_b, score_a, score_b)
# Convert player data to pandas DataFrame
df = pd.DataFrame.from_dict(player_data, orient='index')

# Display player data as a table with players as rows and parameters as columns
st.dataframe(df)

if st.button("Save Player Data"):
  save_data()