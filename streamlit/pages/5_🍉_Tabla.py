import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Stats",
    page_icon=":strawberry:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# filepaths
snapshot_filepath = "./tables/player_snapshots.csv"
player_filepath = "./tables/player_data.csv"

st.title("Tabla General")

# Load and display current table
st.subheader("Tabla")

if os.path.exists(player_filepath):
    current_df = pd.read_csv(player_filepath)
    current_df = current_df.sort_values(by=["Puntos", "PG", "GF"], ascending=False).reset_index(drop=True)
    st.dataframe(current_df, hide_index=True, use_container_width=True)
else:
    st.info("No hay datos disponibles.")

# st.divider()

# # Load snapshot data
# if not os.path.exists(snapshot_filepath):
#     st.warning("No snapshot data available yet. Play at least one matchday to get started.")
#     st.stop()

# snapshots = pd.read_csv(snapshot_filepath)

# if snapshots.empty:
#     st.warning("Snapshot file is empty.")
#     st.stop()

# # Convert date column to datetime
# snapshots["date"] = pd.to_datetime(snapshots["date"])

# # Player selection
# player_names = snapshots["name"].unique()
# selected_player = st.selectbox("Select a player", sorted(player_names))

# # Filter player history
# player_history = snapshots[snapshots["name"] == selected_player].sort_values(by="date")

# # Chart
# st.subheader(f"📊 Point Progression: {selected_player}")
# st.line_chart(player_history.set_index("date")["points"])

# # Optional: Show full snapshot table for player
# with st.expander("🔍 Show full player history"):
#     st.dataframe(player_history.reset_index(drop=True))
