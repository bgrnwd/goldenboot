from pathlib import Path

import polars as pl
import streamlit as st
from great_tables import GT

p = Path(__file__)
parent = p.parent

df = pl.read_csv(f"{parent}/standings.csv")
dfs = df.partition_by("team")

goals = "goals"
goals_label = goals.capitalize()
xgoals = "xgoals"
xgoals_label = "xG"
columns_to_drop = ["player_id", "team"]
sort_by_columns = [goals, xgoals]

wiebe = dfs[0].drop(columns_to_drop).sort(sort_by_columns, descending=True)
wiebe_goals = wiebe.select(pl.sum(goals))
wiebe_xgoals = wiebe.select(pl.sum(xgoals))[xgoals].round(2)

doyle = dfs[1].drop(columns_to_drop).sort(sort_by_columns, descending=True)
doyle_goals = doyle.select(pl.sum(goals))
doyle_xgoals = doyle.select(pl.sum(xgoals))[xgoals].round(2)

gass = dfs[2].drop(columns_to_drop).sort(sort_by_columns, descending=True)
gass_goals = gass.select(pl.sum(goals))
gass_xgoals = gass.select(pl.sum(xgoals))[xgoals].round(2)

scoops = dfs[3].drop(columns_to_drop).sort(sort_by_columns, descending=True)
scoops_goals = scoops.select(pl.sum(goals))
scoops_xgoals = scoops.select(pl.sum(xgoals))[xgoals].round(2)

anders = dfs[4].drop(columns_to_drop).sort(sort_by_columns, descending=True)
anders_goals = anders.select(pl.sum(goals))
anders_xgoals = anders.select(pl.sum(xgoals))[xgoals].round(2)

admin = dfs[5].drop(columns_to_drop).sort(sort_by_columns, descending=True)
admin_goals = admin.select(pl.sum(goals))
admin_xgoals = admin.select(pl.sum(xgoals))[xgoals].round(2)


def build_standings_df(dfs: list[pl.DataFrame]) -> pl.DataFrame:
    participants = []
    goals = []
    xgoals = []
    for df in dfs:
        participant_name = df["team"][0]
        participants.append(participant_name)
        participant_goals = df.select(pl.sum("goals"))["goals"][0]
        participant_xgoals = df.select(pl.sum("xgoals"))["xgoals"][0]
        goals.append(participant_goals)
        xgoals.append(participant_xgoals)
    return pl.DataFrame({"team": participants, "goals": goals, "xG": xgoals})


def create_team_gt(df: pl.DataFrame) -> str:
    return (
        GT(df)
        .fmt_number(columns=xgoals, decimals=2)
        .cols_label(
            {"player_name": "Player", "goals": goals_label, "xgoals": xgoals_label}
        )
        .data_color(columns=[goals, xgoals], palette="Oranges")
        .as_raw_html()
    )


standings = build_standings_df(dfs).sort([goals, xgoals_label], descending=True)
standings_html = (
    GT(standings)
    .fmt_number(columns=xgoals_label, decimals=2)
    .cols_label({"team": "Team", "goals": goals_label})
    .data_color(columns=[goals, xgoals_label], palette="Greens")
    .as_raw_html()
)


st.set_page_config(
    layout="wide",
    page_title="Soccerwise Golden Boot Tracker",
    page_icon="🦉",
)
st.title("Soccerwise Golden Boot Tracker 📈")

st.html(standings_html)

col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns([4, 5, 6])

with st.container():
    with col1:
        st.header("Team Wiebe")
        with st.container():
            metric1, metric2 = st.columns(2)
            with metric1:
                st.metric(label=goals_label, value=wiebe_goals)
            with metric2:
                st.metric(label=xgoals_label, value=wiebe_xgoals)
        st.html(create_team_gt(wiebe))

    with col2:
        st.header("Team Doyle")
        with st.container():
            metric1, metric2 = st.columns(2)
            with metric1:
                st.metric(label=goals_label, value=doyle_goals)
            with metric2:
                st.metric(label=xgoals_label, value=doyle_xgoals)
        st.html(create_team_gt(doyle))

    with col3:
        st.header("Team Gass")
        with st.container():
            metric1, metric2 = st.columns(2)
            with metric1:
                st.metric(label=goals_label, value=gass_goals)
            with metric2:
                st.metric(label=xgoals_label, value=gass_xgoals)
        st.html(create_team_gt(gass))

with st.container():
    with col4:
        st.header("Team Tom/Calen")
        with st.container():
            metric1, metric2 = st.columns(2)
            with metric1:
                st.metric(label=goals_label, value=scoops_goals)
            with metric2:
                st.metric(label=xgoals_label, value=scoops_xgoals)
        st.html(create_team_gt(scoops))

    with col5:
        st.header("Producer Anders")
        with st.container():
            metric1, metric2 = st.columns(2)
            with metric1:
                st.metric(label=goals_label, value=anders_goals)
            with metric2:
                st.metric(label=xgoals_label, value=anders_xgoals)
        st.html(create_team_gt(anders))

    with col6:
        st.header("Team Admin")
        with st.container():
            metric1, metric2 = st.columns(2)
            with metric1:
                st.metric(label=goals_label, value=admin_goals)
            with metric2:
                st.metric(label=xgoals_label, value=admin_xgoals)
        st.html(create_team_gt(admin))

st.caption("Data is updated every Sunday, Monday, and Thursday morning at 3:00AM ET")
st.caption(
    "The wordmarks, logos, trade names, packaging and designs of MLS, SUM, the current and former MLS member clubs are the exclusive property of MLS or their affiliates."
)
st.caption(
    "Data courtesy of [American Soccer Analysis](https://www.americansocceranalysis.com/)"
)
