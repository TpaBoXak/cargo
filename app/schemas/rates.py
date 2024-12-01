from pydantic import BaseModel
from pydantic import Field

class RateBaseSchema(BaseModel):
    title: str
    value: float = Field(
        gt=0, le=1,
        examples = [0.25, 0.35, 0.075],
        description="Значения тарифа должны быть больше 0 и меньше 1"
    )