import sqlite3
from server_py.data.init_db import DB_PATH

def get_last_results(team: str, limit: int = 5):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT match_date, team, opponent, gf, ga, result, goal_diff
        FROM matches 
        WHERE team = ?
        ORDER BY match_date DESC
        LIMIT ?
    """, (team, limit))
    rows = cursor.fetchall()
    conn.close()
    return rows

# if __name__ == "__main__":
#     print(get_last_results("Arsenal"))
