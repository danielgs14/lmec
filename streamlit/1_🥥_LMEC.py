import streamlit as st

st.set_page_config(
    page_title="Liga Mejenguera de Exalumnos Calasancios",
    page_icon=":coconut:",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.header("Liga Mejenguera de Exalumnos Calasancios - LMEC")

col_left1, col_left2, col_center, col_right1, col_right2 = st.columns([1, 1, 2, 1, 1])  # Create three columns
with col_center:
    st.image(
        "https://i.imgur.com/obpJtt4.png",
        width=300
    )

st.subheader("Cómo usar esto")
st.markdown("1. En 🥝 **Jugadores**, pueden añadir nuevos jugadores y editar los que se han ingresado. A los porteros se les puede añadir un emoji para distinguirlos de jugadores.") 
st.markdown("2. Se van a 🥭 **Equipos** y cada jueves se escogen los seis jugadores para cada equipo. Se puede hacer en Gold's antes de la mejenga para asegurarse de que los equipos estén correctos. Pueden escoger el nombre del equipo basado en color de camiseta.")
st.markdown("3. Basado en los jugadores que metieron en 🥭 **Equipos**, les va a salir una lista de jugadores en 🍌 **Goles**. Durante la mejenga, aquí solo tienen que presionar el nombre del jugador para marcar un gol.")
st.markdown("4. Al final, se van a 🍋 **Resultado** para meter el marcador.")
st.markdown("5. En 🍉 **Tabla** van a poder ver la tabla general.")