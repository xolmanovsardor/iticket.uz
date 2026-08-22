from sqlalchemy import select

from src.core.database import AsyncSession
from src.orders.models import Order
from src.ticket_types.models import TicketType


class OrderRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_ticket_type(self, ticket_type_id: str) -> TicketType | None:
        stmt = select(TicketType).where(TicketType.id == ticket_type_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_order(self, order: Order) -> Order:
        self.db.add(order)
        await self.db.commit()
        await self.db.refresh(order)
        return order

    async def get_orders(self, user_id: str) -> list[Order]:
        stmt = select(Order).where(Order.user_id == user_id)
        result = await self.db.execute(stmt)
        return list(result.scalars())
