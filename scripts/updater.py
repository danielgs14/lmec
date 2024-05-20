# imports first
import streamlit as st
import csv 
import pandas as pd

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


# Function to save table as CSV
def save_data(data, filename):
  with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write header row
    writer.writerow(data[next(iter(data))].keys())  # Get headers from first player data
    # Write player data rows
    for player, stats in data.items():
      writer.writerow(stats.values())
  st.success("Player data saved successfully!")


# Function to load table (remains unchanged)
def load_data(filename):
    try:
        # Read CSV data into a pandas dataframe
        df = pd.read_csv(filename)
        # Convert dataframe to dictionary (assuming each row represents a player)
        player_data = df.to_dict(orient='records')
        return player_data
    except FileNotFoundError:
        # Handle case where file doesn't exist (initialize empty data)
        return {}
    except pd.errors.ParserError:
        st.error("Error: Invalid CSV file format.")


# Load data on startup (optional)
player_data = load_data("player_data.json")  # Update filename if needed

# Streamlit interface

# Upload csv
# File uploader for loading CSV data (moved to the top)
uploaded_file = st.file_uploader("Load Player Data (CSV)", type="csv", accept_multiple_fi=False)

if uploaded_file is not None:
    try:
        player_data = load_data(uploaded_file)
        st.success("Player data loaded successfully!")
    except pd.errors.ParserError:
        st.error("Error: Invalid CSV file format.")

# Check if player_data is a dictionary before using .keys()
if isinstance(player_data, dict):
    team_a = st.multiselect("Select Team A Players", player_data.keys())
    team_b = st.multiselect("Select Team B Players", player_data.keys())
else:
    # Handle case where data is not loaded or invalid (display message)
    st.warning("Player data not loaded or invalid. Please load valid CSV data.")

score_a = st.number_input("Team A Score", min_value=0)
score_b = st.number_input("Team B Score", min_value=0)

# Update Table Button
if st.button("Update Table"):
    updater(team_a, team_b, score_a, score_b)

# Save Button (moved to the bottom)
if st.button("Save Player Data (CSV)"):
    save_data(player_data, "player_data.csv")  # Update filename if needed

# Display updated player data table
st.dataframe(player_data)