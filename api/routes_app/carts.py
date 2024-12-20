from uuid import UUID

from fastapi import FastAPI, Depends, HTTPException, APIRouter
from typing import List

from api.auth.token import TokenData
from api.routes_app.auth import get_current_user, get_admin_user
from config.database.queries_table import DatabaseQueries
from schemas.schemas import Cart, CartItemUpdate

from config.project_config import Database
from schemas.schemas import Good

router = APIRouter()

@router.get("/{user_id}", response_model=Cart)
async def get_cart_by_user_id(user_id: UUID,
                              current_admin: TokenData = Depends(get_current_user)):
    print(user_id)
    cart = await DatabaseQueries.get_cart_by_user_id(user_id)
    if cart:
        return cart
    raise HTTPException(status_code=404, detail="Cart not found")


@router.post("/add_good", response_model=dict)
async def add_good_to_cart(item: CartItemUpdate,
                           current_admin: TokenData = Depends(get_current_user)):
    """
    Добавляет товар в корзину.
    """
    print(item.cart_id)
    result = await DatabaseQueries.add_good_to_cart(item.cart_id, item.good_id)
    if not result:
        raise HTTPException(status_code=404, detail="Cart not found or unable to add good")
    return result


@router.post("/remove-good", response_model=dict)
async def remove_good_from_cart(item: CartItemUpdate,
                                current_admin: TokenData = Depends(get_current_user)):
    """
    Удаляет товар из корзины.
    """
    result = await DatabaseQueries.remove_good_from_cart(item.cart_id, item.good_id)
    if not result:
        raise HTTPException(status_code=404, detail="Cart not found or unable to remove good")
    return result


@router.get("/{cart_id}/goods", response_model=List[UUID])
async def get_cart_goods(cart_id: UUID, current_admin: TokenData = Depends(get_current_user)):
    goods = await DatabaseQueries.get_cart_goods(cart_id)  
    if goods is None:
        raise HTTPException(status_code=404, detail="Cart not found or no goods in cart")
    return goods


@router.get("/goods/{good_id}", response_model=Good)
async def get_good(good_id: UUID):
    query = """
        SELECT Id, Title, Price, ImageUrl
        FROM Goods
        WHERE Id = $1;
    """
    good = await Database.fetchrow(query, good_id)
    if good is None:
        raise HTTPException(status_code=404, detail="Good not found")
    return good
