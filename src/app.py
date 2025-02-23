from pathlib import Path

import polars as pl
import streamlit as st

p = Path(__file__)
parent = p.parent

df = pl.read_csv(f"{parent}/standings.csv")
dfs = df.partition_by("team")

st.set_page_config(
    layout="wide",
    page_title="Golden Boot Draft Tracker",
    page_icon="🦉",
    initial_sidebar_state="expanded",
)
st.title("Soccerwise Golden Boot Draft Tracker 📈")

col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns([4, 5, 6])

with st.container():
    with col1:
        st.header("Team Wiebe")
        wiebe = dfs[0]
        wiebe = wiebe.drop(["player_id", "team"])
        with st.container():
            metric1, metric2 = st.columns(2)
            with metric1:
                st.metric(label="Goals", value=wiebe.select(pl.sum("goals")))
            with metric2:
                st.metric(label="xG", value=wiebe.select(pl.sum("xgoals")))
        st.table(wiebe.sort(["goals", "player_name"], descending=True))

    with col2:
        st.header("Team Doyle")
        doyle = dfs[1]
        doyle = doyle.drop(["player_id", "team"])
        with st.container():
            metric1, metric2 = st.columns(2)
            with metric1:
                st.metric(label="Goals", value=doyle.select(pl.sum("goals")))
            with metric2:
                st.metric(label="xG", value=doyle.select(pl.sum("xgoals")))
        st.table(doyle.sort(["goals", "player_name"], descending=True))

    with col3:
        st.header("Team Gass")
        gass = dfs[2]
        gass = gass.drop(["player_id", "team"])
        with st.container():
            metric1, metric2 = st.columns(2)
            with metric1:
                st.metric(label="Goals", value=gass.select(pl.sum("goals")))
            with metric2:
                st.metric(label="xG", value=gass.select(pl.sum("xgoals")))
        st.table(gass.sort(["goals", "player_name"], descending=True))

with st.container():
    with col4:
        st.header("Team Tom/Calen")
        scoops = dfs[3]
        scoops = scoops.drop(["player_id", "team"])
        with st.container():
            metric1, metric2 = st.columns(2)
            with metric1:
                st.metric(label="Goals", value=scoops.select(pl.sum("goals")))
            with metric2:
                st.metric(label="xG", value=scoops.select(pl.sum("xgoals")))
        st.table(scoops.sort(["goals", "player_name"], descending=True))

    with col5:
        st.header("Producer Anders")
        anders = dfs[4]
        anders = anders.drop(["player_id", "team"])
        with st.container():
            metric1, metric2 = st.columns(2)
            with metric1:
                st.metric(label="Goals", value=anders.select(pl.sum("goals")))
            with metric2:
                st.metric(label="xG", value=anders.select(pl.sum("xgoals")))
        st.table(anders.sort(["goals", "player_name"], descending=True))

    with col6:
        st.header("Team Admin")
        admin = dfs[5]
        admin = admin.drop(["player_id", "team"])
        with st.container():
            metric1, metric2 = st.columns(2)
            with metric1:
                st.metric(label="Goals", value=admin.select(pl.sum("goals")))
            with metric2:
                st.metric(label="xG", value=admin.select(pl.sum("xgoals")))
        st.table(admin.sort(["goals", "player_name"], descending=True))

st.caption("Data is updated every Monday and Thursday morning at 3:00AM ET")
st.caption(
    "The wordmarks, logos, trade names, packaging and designs of MLS, SUM, the current and former MLS member clubs are the exclusive property of MLS or their affiliates."
)
st.caption(
    "Data courtesy of [American Soccer Analysis](https://www.americansocceranalysis.com/)"
)
