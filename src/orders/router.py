from fastapi import APIRouter, Depends

from src.core.database import get_db, AsyncSession
from src.auth.dependencies import get_current_active_user
from src.orders.models import Order
from src.orders.repository import OrderRepository
from src.orders.schemas import OrderCreate, OrderResponse, OrderResponseList
from src.orders.service import OrderService
from src.users.models import User


router = APIRouter()


@router.post("/", response_model=OrderResponse)
async def create_order(
    data: OrderCreate,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Order:
    service = OrderService(OrderRepository(db))
    return await service.create_order(data, user)


@router.get("/", response_model=OrderResponseList)
async def get_order_list(
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> OrderResponseList:
    service = OrderService(OrderRepository(db))
    orders = await service.get_orders(user)
    return OrderResponseList(orders=orders)  # type: ignore
