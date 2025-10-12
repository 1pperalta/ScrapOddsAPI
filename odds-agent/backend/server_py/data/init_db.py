import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "matches.db")

def init_db():
    print("📁 Directorio base:", BASE_DIR)
    print("🗂️ Ruta de la base de datos:", DB_PATH)

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    print("✅ Carpeta verificada/creada")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    print("🔌 Conexión a SQLite establecida")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_date TEXT,
        day TEXT,
        match_hour INTEGER,
        week INTEGER,
        country TEXT,
        season TEXT,
        league TEXT,
        venue TEXT,
        team TEXT,
        gf INTEGER,
        ga INTEGER,
        opponent TEXT,
        result TEXT,
        goal_diff INTEGER
    )
    """)
    print("📄 Tabla matches creada/verificada")

    conn.commit()
    conn.close()
    print(f"✅ Base de datos creada en {DB_PATH}")

if __name__ == "__main__":
    init_db()
