from fastapi import APIRouter, HTTPException

from app.crud.product import ProductCRUD
from app.schemas.product import ProductResponse, ErrorResponse, ProductQuery


product_crud = ProductCRUD()


router = APIRouter()



@router.post("/shelf-life", response_model=ProductResponse, responses={404: {"model": ErrorResponse}})
async def get_product_shelf_life(product_query: ProductQuery):
    try:
        item_name_clean = product_query.ItemName.replace('"', '').replace("'", "")
        description_clean = product_query.Description.replace('"', '').replace("'", "")
        combined_query = f"{description_clean} {item_name_clean}"

        
        shelf_life = product_crud.get_shelf_life_by_name(combined_query)
        
        if shelf_life is None:
            raise HTTPException(
                status_code=404,
                detail=f"Товар не найден или срок годности не указан"
            )
        
        return ProductResponse(LifeTime=shelf_life)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Внутренняя ошибка сервера: {str(e)}"
        )