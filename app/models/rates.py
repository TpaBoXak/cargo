from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Date


from datetime import date

from .base import Base

class Rate(Base):
    __tablename__ = "rates"
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    date_of_action: Mapped[date] = mapped_column(Date, nullable=False)