from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status

from src.orders.models import Order
from src.orders.repository import OrderRepository
from src.orders.schemas import OrderCreate
from src.users.models import User


class OrderService:
    def __init__(self, repository: OrderRepository) -> None:
        self.repository = repository

    async def create_order(self, data: OrderCreate, user: User) -> Order:
        ticket_type = await self.repository.get_ticket_type(str(data.ticket_type_id))
        if ticket_type is None or not ticket_type.is_active:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket turi topilmadi.")

        available = (ticket_type.quantity_total or 0) - (ticket_type.quantity_sold or 0)
        if data.quantity > available:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Yetarli joy yo'q.")

        ticket_type.quantity_sold = (ticket_type.quantity_sold or 0) + data.quantity
        order = Order(
            user_id=str(user.id),
            ticket_type_id=str(data.ticket_type_id),
            quantity=data.quantity,
            unit_price=ticket_type.price,
            total_amount=ticket_type.price * data.quantity,
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=15),
        )
        return await self.repository.create_order(order)

    async def get_orders(self, user: User) -> list[Order]:
        return await self.repository.get_orders(str(user.id))
