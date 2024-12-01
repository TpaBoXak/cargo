from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy import ForeignKey


from datetime import datetime

from .base import Base

class Rate(Base):
    __tablename__ = "rates"
    title: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    date_of_action: Mapped[datetime] = mapped_column(DateTime, nullable=False,
            server_default=func.now())