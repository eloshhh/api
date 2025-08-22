from fastapi import APIRouter
from fastapi.models.categories import Category
from fastapi.services import categories as category_service

router = APIRouter()

@router.get("/categories")
def get_categories():
    return category_service.get_all_categories()

@router.get("/categories/{category_id}")
def get_category(category_id: int):
    category = category_service.get_category_by_id(category_id)
    if category:
        return category
    return {"error": "Category not found"}

@router.post("/categories")
def add_category(category: Category):
    result = category_service.add_category(category.name)
    if result:
        return result
    return {"error": "Bu kategori zaten mevcut"}

@router.put("/categories/{category_id}")
def update_category(category_id: int, category: Category):
    success = category_service.update_category(category_id, category.name)
    return {"message": "Updated"} if success else {"error": "Not found"}

@router.delete("/categories/{category_id}")
def delete_category(category_id: int):
    success = category_service.delete_category(category_id)
    return {"message": "Deleted"} if success else {"error": "Not found"}
