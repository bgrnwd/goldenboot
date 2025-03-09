import re
from datetime import datetime
from pathlib import Path

import polars as pl
from itscalledsoccer.client import AmericanSoccerAnalysis

p: Path = Path(__file__)
root: Path = p.parent.parent.parent
standings_csv_file: str = f"{root}/src/standings.csv"
standings_py_file: str = f"{root}/src/standings.py"

df: pl.DataFrame = pl.read_csv(standings_csv_file)
players: pl.Series = df["player_id"]
client: AmericanSoccerAnalysis = AmericanSoccerAnalysis(lazy_load=False)

for index, player in enumerate(players.to_list()):
    if player:
        xgoal: pl.DataFrame = client.get_player_xgoals(
            player_ids=player, leagues="mls", season_name="2025"
        )
        df[index, "goals"] = xgoal.get("goals", 0)
        df[index, "xgoals"] = xgoal.get("xgoals", 0)
        df[index, "assists"] = xgoal.get("primary_assists", 0)

df.write_csv(standings_csv_file)
with open(standings_py_file, "r") as f:
    content = f.read()
updated = datetime.now().strftime("%A %B %d, %Y at %I:%M:%S %p")
new_content = re.sub(
    "\\w+day \\w+ \\d{2}, \\d{4} at \\d{2}:\\d{2}:\\d{2} [AP]M", updated, content
)
with open(standings_py_file, "w+") as f:
    f.write(new_content)
