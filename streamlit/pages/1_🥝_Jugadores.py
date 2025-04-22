import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Jugadores",
    page_icon=":kiwi:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# filepaths
player_filepath = "./tables/player_data.csv"

columns = ["Nombre", "Puntos", "PJ", "PG", "PP", "PE", "GF", "GC", "GInd"]

def load_player_data():
def load_player_data():
    if os.path.exists(player_filepath):
        try:
            df = pd.read_csv(player_filepath)
            for col in columns:
                if col not in df.columns:
                    df[col] = 0 if col != "name" else ""
            return df[columns]
        except pd.errors.EmptyDataError:
            return pd.DataFrame(columns=columns)
    else:
        return pd.DataFrame(columns=columns)


def save_player_data(df):
    df.to_csv(player_filepath, index=False)

st.title("🍍 Jugadores")

# Load existing or empty DataFrame
player_df = load_player_data()

# Form to add a new player
with st.form("add_player_form"):
    st.subheader("Añadir jugadores")
    name = st.text_input("Nombre")
    submit = st.form_submit_button("Añadir jugadores")
    
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
                "GInd": 0,
            }
            player_df = pd.concat([player_df, pd.DataFrame([new_row])], ignore_index=True)
            save_player_data(player_df)
            st.success(f"Jugador '{name}' añadido.")
        elif name in player_df["Nombre"].values:
            st.warning("Ya existe el jugador.")
        else:
            st.error("Añada un nombre.")

# Display the current player table
st.subheader("Lista de Jugadores Actuales")
st.dataframe(
    player_df.sort_values(by=["Puntos", "PG", "GF"], ascending=False)
    ,hide_index=True
    ,use_container_width=True
)