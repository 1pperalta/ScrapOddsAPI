import json
from pathlib import Path
from typing import Dict
from .config import DATA_PATH

try:
    import soccerdata as sd
except ImportError:
    sd = None

class SoccerDataCollector:
    def __init__(self):
        self.stats_path = DATA_PATH / "soccerdata"
        self.stats_path.mkdir(parents=True, exist_ok=True)
        # Mapping config leagues to soccerdata leagues
        self.league_map = {
            "Premier League": "ENG-Premier League",
            "La Liga": "ESP-La Liga",
            "Serie A": "ITA-Serie A",
            "Bundesliga": "GER-Bundesliga",
            "Ligue 1": "FRA-Ligue 1",
            "Champions League": "INT-Champions League"
        }

    def collect_team_stats(self) -> Dict:
        if not sd:
            print("soccerdata library is not installed. Skipping advanced stats collection.")
            return {}

        all_stats = {}
        for config_name, sd_name in self.league_map.items():
            print(f"  Fetching advanced stats for {config_name} using FBref...")
            try:
                # FBref standard and shooting stats
                fbref = sd.FBref(leagues=sd_name, seasons=2024)
                
                # dropmulti index, flatten columns
                std_stats = fbref.read_team_season_stats(stat_type="standard")
                sht_stats = fbref.read_team_season_stats(stat_type="shooting")
                
                std_stats.columns = ['_'.join(col).strip() for col in std_stats.columns.values]
                sht_stats.columns = ['_'.join(col).strip() for col in sht_stats.columns.values]
                
                if config_name not in all_stats:
                    all_stats[config_name] = {}

                for index, row in std_stats.iterrows():
                    team_name = index[2]
                    
                    stats_dict = {
                        "possession_pct": float(row.get('Poss_', 0)),
                        "goals_per_90": float(row.get('Per 90 Minutes_Gls', 0)),
                        "assists_per_90": float(row.get('Per 90 Minutes_Ast', 0)),
                    }
                    
                    # try to get shooting stats
                    try:
                        sht_row = sht_stats.loc[index]
                        stats_dict.update({
                            "shots_per_90": float(sht_row.get('Standard_Sh/90', 0)),
                            "shots_on_target_per_90": float(sht_row.get('Standard_SoT/90', 0)),
                            "goals_per_shot": float(sht_row.get('Standard_G/Sh', 0))
                        })
                    except KeyError:
                        pass
                        
                    all_stats[config_name][team_name] = stats_dict
            except Exception as e:
                print(f"  Failed to fetch advanced stats for {config_name}: {e}")
                
        # Save to file
        output_file = self.stats_path / "team_advanced_stats.json"
        with open(output_file, "w") as f:
            json.dump(all_stats, f, indent=2)
            
        print(f"  Saved advanced stats to {output_file}")
        return all_stats

