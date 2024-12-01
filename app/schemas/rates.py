from pydantic import BaseModel
from pydantic import Field
from datetime import date


class RateWithoutDateSchema(BaseModel):
    cargo_type: str
    rate: float = Field(
        ge=0, le=1,
        examples = [0.25, 0.35, 0.075],
        description="Значения тарифа должны быть больше 0 и меньше или равно 1"
    )

class RateWithoutRate(BaseModel):
    cargo_type: str
    action_date: date = Field(
        examples=["2024-12-01"],
        description="Дата в формате YYYY-MM-DD"
    )

class RateBaseSchema(RateWithoutDateSchema):
    action_date: date = Field(
        examples=["2024-12-01"],
        description="Дата в формате YYYY-MM-DD"
    )

class CargoSchema(BaseModel):
    action_date: date = Field(
        examples=["2024-12-01"],
        description="Дата в формате YYYY-MM-DD"
    )
    declared_price: float = Field(
        ge=0,
        examples = [100000],
        description="Значения объявленной стоимости должны быть больше 0"
    )
    cargo_type: str = Field(
        examples=["Glass", "Other", "Wood", "Food"],
        description="Тип груза"
    )