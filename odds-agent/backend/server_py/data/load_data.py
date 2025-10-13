import csv
import sqlite3
import os
from init_db import init_db, DB_PATH

def load_csv_to_db():
    init_db()

    # Ruta absoluta del CSV
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(BASE_DIR, "leagues_matches.csv")

    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"❌ No se encontró el archivo CSV en {csv_file}")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open(csv_file, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute("""
            INSERT INTO matches 
            (match_date, day, match_hour, week, country, season, league, venue, team, gf, ga, opponent, result, goal_diff)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row["match_date"],
                row["day"],
                row["match_hour"],
                row["week"],
                row["country"],
                row["season"],
                row["league"],
                row["venue"],
                row["team"],
                row["gf"],
                row["ga"],
                row["opponent"],
                row["result"],
                row["goal_diff"]
            ))
    conn.commit()
    conn.close()
    print("✅ CSV cargado a SQLite")

if __name__ == "__main__":
    load_csv_to_db()

