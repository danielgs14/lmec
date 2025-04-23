import streamlit as st
import pandas as pd
from helpers.sheets_handler import read_player_data, write_player_data

st.set_page_config(
    page_title="Jugadores",
    page_icon=":kiwi-fruit:",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Define the Google Sheet name
sheet_name = "player_data"

# Fetch player data from Google Sheets
player_data = read_player_data(sheet_name)
player_df = pd.DataFrame(player_data)

# columns = ["Nombre", "Puntos", "PJ", "PG", "PP", "PE", "GF", "GC", "GInd"]

st.title("🍍 Jugadores")

# Form to add a new player
with st.form("add_player_form"):
    st.subheader("Añadir nuevo jugador")
    name = st.text_input("Nombre del jugador")
    submit = st.form_submit_button("Añadir jugador")
    
    if submit:
        if name and name not in player_df["Nombre"].values:
            new_row = {
                "Nombre": name,
                "Puntos": 0,
                "PJ": 0,
                "PG": 0,
                "PE": 0,
                "PP": 0,
                "GF": 0,
                "GC": 0,
                "GInd": 0
            }
            player_df = pd.concat([player_df, pd.DataFrame([new_row])], ignore_index=True)

            write_player_data(sheet_name, player_df.to_dict(orient="records"))
            st.success(f"Jugador '{name}' añadido.")
        elif name in player_df["Nombre"].values:
            st.warning("Ya existe el jugador.")
        else:
            st.error("Ingresar nombre.")

st.subheader("Lista Actual de Jugadores")
st.dataframe(
    player_df.sort_values(by=["Puntos", "PG", "GInd", "GF"], ascending=False),hide_index=True,use_container_width=True)
