from pathlib import Path

import polars as pl
from itscalledsoccer.client import AmericanSoccerAnalysis

p = Path(__file__)
root = p.parent.parent.parent
standings_file = f"{root}/src/standings.csv"

df = pl.read_csv(standings_file)
players = df["player_name"]
client = AmericanSoccerAnalysis(lazy_load=False)

for index, player in enumerate(players.to_list()):
    xgoal = client.get_player_xgoals(
        player_names=player, leagues="mls", season_name="2025"
    )
    df[index, "player_id"] = xgoal.get("player_id")
    df[index, "goals"] = xgoal.get("goals", 0)
    df[index, "xgoals"] = xgoal.get("xgoals", 0)

df.write_csv(standings_file)
