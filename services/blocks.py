from api.config.database import get_db
from api.config.logger import logger

def get_all_blocks():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT b.id, b.category_id, b.title, b.content, c.name as category_name
            FROM blocks b
            JOIN categories c ON b.category_id = c.id
        """)
        rows = cursor.fetchall()
    logger.info("Tüm bloklar getirildi")
    return [dict(row) for row in rows]

def add_block(category_id: int, title: str, content: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM categories WHERE id = ?", (category_id,))
        category = cursor.fetchone()
        if not category:
            logger.warning(f"Geçersiz kategori id ile blok ekleme denemesi: {category_id}")
            return None

        cursor.execute(
            "INSERT INTO blocks (category_id, title, content) VALUES (?, ?, ?)", 
            (category_id, title, content)
        )
        conn.commit()
        new_id = cursor.lastrowid
    logger.info(f"Blok eklendi: id={new_id}, kategori={category_id}, başlık={title}")
    return {"id": new_id, "category_id": category_id, "title": title, "content": content}

def update_block(block_id: int, category_id: int, title: str, content: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE blocks SET category_id = ?, title = ?, content = ? WHERE id = ?", 
            (category_id, title, content, block_id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            logger.warning(f"Güncellenmek istenen blok bulunamadı: id={block_id}")
            return None
    logger.info(f"Blok güncellendi: id={block_id}, kategori={category_id}, başlık={title}")
    return {"id": block_id, "category_id": category_id, "title": title, "content": content}

def delete_block(block_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM blocks WHERE id = ?", (block_id,))
        conn.commit()
        if cursor.rowcount == 0:
            logger.warning(f"Silinmek istenen blok bulunamadı: id={block_id}")
            return False
    logger.info(f"Blok silindi: id={block_id}")
    return True
