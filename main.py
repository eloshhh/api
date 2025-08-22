from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import logging

app = FastAPI()

# ---- Logger ayarı ----
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("myapp")

# ---- Veri modeli ----
class Category(BaseModel):
    name: str
    
class Block(BaseModel):
    category_id: int   # önce category
    title: str
    content: str

# ---- DB yardımcı fonksiyon ----
def get_db():
    conn = sqlite3.connect("mydb.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---- Tabloyu oluştur ----
with get_db() as conn:
    # Category tablosu
    conn.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    # Blocks tablosu (kategoriye bağlı)
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
    
# ---- API ----

# 1) GET - Tüm blokları getir
@app.get("/blocks")
def get_blocks():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, category, title, content FROM blocks")
        rows = cursor.fetchall()
    return [dict(row) for row in rows]

# 2) POST - Yeni blok ekle
@app.post("/blocks")
def add_block(block: Block):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO blocks (category, title, content) VALUES (?, ?, ?)", 
            (block.category, block.title, block.content)
        )
        conn.commit()
        new_id = cursor.lastrowid
    return {"id": new_id, "category": block.category, "title": block.title, "content": block.content}

# 3) PUT - Var olan bloğu güncelle
@app.put("/blocks/{block_id}")
def update_block(block_id: int, block: Block):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE blocks SET category = ?, title = ?, content = ? WHERE id = ?", 
            (block.category, block.title, block.content, block_id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return {"error": f"Block {block_id} not found"}
    return {"id": block_id, "category": block.category, "title": block.title, "content": block.content}

# 4) DELETE - Bloğu sil
@app.delete("/blocks/{block_id}")
def delete_block(block_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM blocks WHERE id = ?", (block_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return {"error": f"Block {block_id} not found"}
    return {"message": f"Block {block_id} deleted"}
