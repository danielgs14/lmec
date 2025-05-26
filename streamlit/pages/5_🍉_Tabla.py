import streamlit as st
import pandas as pd
from helpers.sheets_handler import read_snapshot_data

st.set_page_config(
    page_title="Stats",
    page_icon=":watermelon:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sheets
snapshot_sheet_name = "snapshot_data"

st.title("🏆 Tabla General")

snapshot_df = pd.DataFrame(read_snapshot_data(snapshot_sheet_name))
if snapshot_df.empty:
    st.warning("No hay datos históricos aún. Juegue un partido para comenzar.")
    st.stop()

snapshot_df["partido"] = pd.to_datetime(snapshot_df["partido"], errors="coerce")

numeric_cols = ["Puntos", "PJ", "PG", "PE", "PP", "GF", "GC", "GInd"]
snapshot_df[numeric_cols] = snapshot_df[numeric_cols].apply(pd.to_numeric, errors="coerce")

snapshot_df = snapshot_df.sort_values(by=["Nombre", "partido"])
snapshot_df["delta_puntos"] = snapshot_df.groupby("Nombre")["Puntos"].diff()

latest_date = snapshot_df["partido"].max()
latest_snapshot = snapshot_df[snapshot_df["partido"] == latest_date].copy()

def points_arrows(row):
    if pd.isna(row["delta_puntos"]):
        return str(int(row["Puntos"]))
    elif row["delta_puntos"] > 0:
        return f'{int(row["Puntos"])} ⬆️'
    elif row["delta_puntos"] < 0:
        return f'{int(row["Puntos"])} ⬇️'
    else:
        return f'{int(row["Puntos"])} ↔️'

latest_snapshot["Puntaje"] = latest_snapshot.apply(points_arrows, axis=1)
latest_snapshot = latest_snapshot.sort_values(by=["Puntos", "PG", "GInd", "GF"], ascending=False).reset_index(drop=True)

latest_snapshot["Nombre_clean"] = latest_snapshot["Nombre"]
medals = ["🥇", "🥈", "🥉"]
for i in range(min(3, len(latest_snapshot))):
    latest_snapshot.at[i, "Nombre"] = f"{medals[i]} {latest_snapshot.at[i, 'Nombre']}"

latest_stats = snapshot_df.sort_values("partido").groupby("Nombre", as_index=False).last()
latest_stats["Puntos_por_PJ"] = latest_stats["Puntos"] / latest_stats["PJ"]
latest_stats["Puntos_por_PJ"] = latest_stats["Puntos_por_PJ"].fillna(0)
latest_stats["DIF"] = latest_stats["GF"] - latest_stats["GC"]
latest_stats["Rendimiento"] = latest_stats["Puntos"] / (latest_stats["PJ"] * 3) * 100
latest_stats["Rendimiento"] = latest_stats["Rendimiento"].fillna(0).round(2)

latest_snapshot["DIF"] = latest_snapshot["Nombre_clean"].map(latest_stats.set_index("Nombre")["DIF"])
latest_snapshot["Puntos_por_PJ"] = latest_snapshot["Nombre_clean"].map(latest_stats.set_index("Nombre")["Puntos_por_PJ"])
latest_snapshot["Rendimiento"] = latest_snapshot["Nombre_clean"].map(latest_stats.set_index("Nombre")["Rendimiento"])

columns_to_show = [
    "Nombre", "Puntaje", "PJ", "PG", "PE", "PP", "GInd",
    "GF", "GC", "DIF", "Puntos_por_PJ", "Rendimiento"
]
columns_renamed = {
    "Puntos_por_PJ": "Puntos por PJ",
    "Rendimiento": "Rendimiento (%)"
}
st.dataframe(
    latest_snapshot[columns_to_show].rename(columns=columns_renamed),
    hide_index=True,
    use_container_width=True
)

filtered_avg_stats = latest_stats[latest_stats["PJ"] >= 3].copy()

def get_top_players(df, column, mode="max"):
    if df.empty:
        return "", 0
    value = df[column].max() if mode == "max" else df[column].min()
    top_players = df[df[column] == value]
    names = ", ".join(top_players["Nombre"].tolist())
    return names, value

# ------------------------------------
st.divider()
# ------------------------------------

st.subheader("Highlights de la tabla")

cols = st.columns(2)
pj_name, pj_val = get_top_players(latest_stats, "PJ")
pg_name, pg_val = get_top_players(latest_stats, "PG")
cols[0].metric("Más partidos jugados", pj_name, f'{int(pj_val)} PJ')
cols[1].metric("Más partidos ganados", pg_name, f'{int(pg_val)} PG')

cols = st.columns(2)
gind_name, gind_val = get_top_players(latest_stats, "GInd")
avg_name, avg_val = get_top_players(filtered_avg_stats, "Puntos_por_PJ")
cols[0].metric("Más goles personales", gind_name, f'{int(gind_val)} GInd')
cols[1].metric("Más puntos por partido", avg_name, f'{avg_val:.2f} pts/juego')

# ------------------------------------
st.divider()
# ------------------------------------

st.subheader("Otros datos")

stat_options = {
    "Partidos Jugados (PJ)": "PJ",
    "Partidos Ganados (PG)": "PG",
    "Partidos Empatados (PE)": "PE",
    "Partidos Perdidos (PP)": "PP",
    "Goles a favor (GF)": "GF",
    "Goles en contra (GC)": "GC",
    "Goles personales (GInd)": "GInd",
    "Diferencia de goles (DIF)": "DIF",
    "Puntos por partido (Puntos_por_PJ)": "Puntos_por_PJ",
    "Rendimiento (%)": "Rendimiento"
}

col1, col2 = st.columns(2)
selected_stat_label = col1.selectbox("Estadística", list(stat_options.keys()))
selected_stat_col = stat_options[selected_stat_label]
selection_mode = col2.radio("Tipo", ["Más", "Menos"], horizontal=True)

mode = "max" if selection_mode == "Más" else "min"
stat_name, stat_val = get_top_players(filtered_avg_stats, selected_stat_col, mode)

if selected_stat_col in ["Puntos_por_PJ"]:
    value_str = f"{stat_val:.2f} pts/juego"
elif selected_stat_col == "Rendimiento":
    value_str = f"{stat_val * 100:.2f} %"
else:
    value_str = f"{int(stat_val)}"

st.metric(f"{selection_mode} {selected_stat_label}", stat_name, value_str)
