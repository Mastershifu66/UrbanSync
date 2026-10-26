from datetime import datetime, timezone
from sqlalchemy import String, Integer, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base
class Complaint(Base):
    __tablename__="complaints"
    id: Mapped[int]=mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str]=mapped_column(String(160), nullable=False)
    category: Mapped[str]=mapped_column(String(60), default="General")
    location: Mapped[str]=mapped_column(String(160), default="Jaipur")
    description: Mapped[str]=mapped_column(Text, default="")
    status: Mapped[str]=mapped_column(String(40), default="Submitted")
    department: Mapped[str]=mapped_column(String(80), default="Citizen Services")
    priority: Mapped[str]=mapped_column(String(20), default="Medium")
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
