from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base, UUIDMixin, TimestampMixin
if TYPE_CHECKING:
    from src.ticket_types.models import TicketType
    from src.users.models import User


class Order(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "orders"

    user_id: Mapped[str] = mapped_column("user_id", ForeignKey("users.id"))
    ticket_type_id: Mapped[str] = mapped_column("ticket_type_id", ForeignKey("ticket_types.id"))
    quantity: Mapped[int] = mapped_column("quantity", nullable=False)
    unit_price: Mapped[float] = mapped_column("unit_price", nullable=False)
    total_amount: Mapped[float] = mapped_column("total_amount", nullable=False)
    status: Mapped[str] = mapped_column("status", nullable=False, default="pending")
    expires_at: Mapped[datetime] = mapped_column("expires_at", nullable=False)

    user: Mapped["User"] = relationship(foreign_keys=[user_id])
    ticket_type: Mapped["TicketType"] = relationship(foreign_keys=[ticket_type_id])
