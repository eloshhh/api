from pydantic import BaseModel

class Block(BaseModel):
    category_id: int
    title: str
    content: str
