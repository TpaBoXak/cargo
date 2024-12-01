from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy import ForeignKey


from datetime import datetime

from .base import Base

class Rate(Base):
    __tablename__ = "rates"
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    value: Mapped[int] = mapped_column(Integer, nullable=False)
    time_created: Mapped[datetime] = mapped_column(DateTime, nullable=False,
            server_default=func.now())