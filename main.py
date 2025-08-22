from app import FastAPI
from app.config.database import get_db
from app.routers import categories, blocks

app = FastAPI()

# ---- Tabloları oluştur (senin eski kodun buraya gelecek) ----
with get_db() as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS blocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER,
            title TEXT,
            content TEXT,
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
    """)
    conn.commit()

# ---- Routerları ekle ----
app.include_router(categories.router)
app.include_router(blocks.router)
