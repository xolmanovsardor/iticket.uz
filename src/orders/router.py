from fastapi import APIRouter, Depends

from src.auth.dependencies import get_current_active_user
from src.core.database import AsyncSession, get_db
from src.orders.models import Order
from src.orders.repository import OrderRepository
from src.orders.schemas import OrderCreate, OrderResponse, OrderResponseList
from src.orders.service import OrderService
from src.users.models import User

router = APIRouter()


@router.post("/", response_model=OrderResponse)
async def create_order(
    data: OrderCreate,
    user: User = Depends(get_current_active_user),  # noqa: B008
    db: AsyncSession = Depends(get_db),  # noqa: B008
) -> Order:
    service = OrderService(OrderRepository(db))
    return await service.create_order(data, user)


@router.get("/", response_model=OrderResponseList)
async def get_order_list(
    user: User = Depends(get_current_active_user),  # noqa: B008
    db: AsyncSession = Depends(get_db),  # noqa: B008
) -> OrderResponseList:
    service = OrderService(OrderRepository(db))
    orders = await service.get_orders(user)
    return OrderResponseList(orders=orders)  # type: ignore
