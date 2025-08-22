from api import APIRouter
from app.models.blocks import Block
from app.services import blocks as block_service

router = APIRouter()

@router.get("/blocks")
def get_blocks():
    return block_service.get_all_blocks()

@router.post("/blocks")
def add_block(block: Block):
    result = block_service.add_block(block.category_id, block.title, block.content)
    if result:
        return result
    return {"error": "Geçersiz kategori id"}

@router.put("/blocks/{block_id}")
def update_block(block_id: int, block: Block):
    result = block_service.update_block(block_id, block.category_id, block.title, block.content)
    if result:
        return result
    return {"error": f"Block {block_id} not found"}

@router.delete("/blocks/{block_id}")
def delete_block(block_id: int):
    success = block_service.delete_block(block_id)
    return {"message": "Deleted"} if success else {"error": f"Block {block_id} not found"}
