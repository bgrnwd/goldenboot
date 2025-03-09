import streamlit as st

st.set_page_config(
    layout="wide",
    page_title="Soccerwise Golden Boot Tracker",
    page_icon="🦉",
)

tracker = st.Page(
    "standings.py",
    title="Standings",
    icon="📊",
)
about = st.Page("about.py", title="About", icon="ℹ️")

pg = st.navigation([tracker, about])
pg.run()
