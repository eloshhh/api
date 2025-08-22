from fastapi.config.database import get_db
from fastapi.config.logger import logger

def get_all_categories():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM categories")
        rows = cursor.fetchall()
    logger.info("Tüm kategoriler getirildi")
    return [dict(row) for row in rows]

def get_category_by_id(category_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM categories WHERE id = ?", (category_id,))
        row = cursor.fetchone()
    return dict(row) if row else None

def add_category(name: str):
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))
            conn.commit()
            new_id = cursor.lastrowid
            logger.info(f"Kategori eklendi: {name} (id={new_id})")
            return {"id": new_id, "name": name}
        except:
            logger.warning(f"Kategori zaten mevcut: {name}")
            return None

def update_category(category_id: int, name: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE categories SET name = ? WHERE id = ?", (name, category_id))
        conn.commit()
        return cursor.rowcount > 0

def delete_category(category_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        conn.commit()
        return cursor.rowcount > 0
