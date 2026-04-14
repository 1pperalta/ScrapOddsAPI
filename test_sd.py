import soccerdata as sd
fbref = sd.FBref(leagues="ENG-Premier League", seasons=2024)
stats = fbref.read_team_season_stats(stat_type="standard")
print(stats.columns)
print(stats.head())
