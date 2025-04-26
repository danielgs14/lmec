import streamlit as st
import pandas as pd
from helpers.sheets_handler import read_player_data, write_player_data

st.set_page_config(
    page_title="Jugadores",
    page_icon=":kiwi-fruit:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# sheet and df data
sheet_name = "player_data"
player_data = read_player_data(sheet_name)
player_df = pd.DataFrame(player_data)

# columns = ["Nombre", "Puntos", "PJ", "PG", "PP", "PE", "GF", "GC", "GInd"]

#st stuff
st.title("🍍 Jugadores")

# new player form
with st.form("add_player_form"):
    st.subheader("Añadir nuevo jugador")
    name = st.text_input("Nombre del jugador")
    submit = st.form_submit_button("Añadir jugador")
    
    if submit:
        if name and name not in player_df["Nombre"].values:
            new_row = {
                "Nombre": name,
                "PJ": 0,
                "PG": 0,
                "PE": 0,
                "PP": 0,
                "GF": 0,
                "GC": 0,
                "GInd": 0,
                "Puntos": 0
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

st.divider()
st.subheader("Editar Jugadores")

if player_df.empty:
    st.warning("No hay jugadores para editar.")
else:
    selected_player = st.selectbox("Selecciona un jugador", player_df["Nombre"].unique())

    if selected_player:
        current_data = player_df[player_df["Nombre"] == selected_player].iloc[0]

        new_name = st.text_input("Nombre", value=current_data["Nombre"])
        new_GF = st.number_input("Goles a favor", value=int(current_data["GF"]))
        new_GC = st.number_input("Goles en contra", value=int(current_data["GC"]))
        new_GInd = st.number_input("Goles individuales", value=int(current_data["GInd"]))

        if st.button("Guardar cambios"):
            idx = player_df[player_df["Nombre"] == selected_player].index[0]
            player_df.at[idx, "Nombre"] = new_name
            player_df.at[idx, "GF"] = new_GF
            player_df.at[idx, "GC"] = new_GC
            player_df.at[idx, "GInd"] = new_GInd

            # Convert back to list of dicts and write
            write_player_data(sheet_name, player_df.to_dict(orient="records"))
            st.success("Jugador actualizado exitosamente.")