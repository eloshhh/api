from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# ---- Veritabanı ----
conn = sqlite3.connect("mydb.db")
conn.execute("CREATE TABLE IF NOT EXISTS blocks (id INTEGER PRIMARY KEY, title TEXT, content TEXT)")
conn.commit()
conn.close()
conn = sqlite3.connect("mydb.db")
cursor = conn.cursor()

# ---- Veri modeli ----
class Block(BaseModel):
    title: str
    content: str

# ---- API ----

# 1) GET - Tüm blokları getir
@app.get("/blocks")
def get_blocks():
    cursor.execute("SELECT id, title, content FROM blocks")
    rows = cursor.fetchall()
    conn.close()
    return rows   # [(id, title, content), ...]

# 2) POST - Yeni blok ekle
@app.post("/blocks")
def add_block(block: Block):
    cursor.execute("INSERT INTO blocks (title, content) VALUES (?, ?)", (block.title, block.content))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {"id": new_id, "title": block.title, "content": block.content}

# 3) PUT - Var olan bloğu güncelle
@app.put("/blocks/{block_id}")
def update_block(block_id: int, block: Block):
    cursor.execute("UPDATE blocks SET title = ?, content = ? WHERE id = ?", (block.title, block.content, block_id))
    conn.commit()
    conn.close()
    return {"id": block_id, "title": block.title, "content": block.content}

# 4) DELETE - Bloğu sil
@app.delete("/blocks/{block_id}")
def delete_block(block_id: int):
    cursor.execute("DELETE FROM blocks WHERE id = ?", (block_id,))
    conn.commit()
    conn.close()
    return {"message": f"Block {block_id} deleted"}
