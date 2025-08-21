from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

# Uygulamayı başlat
app = FastAPI()

# -------- Veritabanı bağlantısı --------
def get_db():
    conn = sqlite3.connect("mydb.db")  # mydb.db dosyası oluşacak
    conn.row_factory = sqlite3.Row
    return conn

# Tabloyu oluştur (ilk çalıştırmada)
conn = get_db()
conn.execute("CREATE TABLE IF NOT EXISTS blocks (id INTEGER PRIMARY KEY, title TEXT, content TEXT)")
conn.commit()
conn.close()

# -------- Veri modeli --------
class Block(BaseModel):
    title: str
    content: str

# -------- API --------

# Tüm blokları getir
@app.get("/blocks")
def get_blocks():
    conn = get_db()
    blocks = conn.execute("SELECT * FROM blocks").fetchall()
    conn.close()
    return [dict(b) for b in blocks]

# Yeni blok ekle
@app.post("/blocks")
def add_block(block: Block):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO blocks (title, content) VALUES (?, ?)", (block.title, block.content))
    conn.commit()
    block_id = cur.lastrowid
    conn.close()
    return {"id": block_id, "title": block.title, "content": block.content}
