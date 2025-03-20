from datetime import datetime
from pydantic import BaseModel, Field


class CoilAddSchema(BaseModel):
    length: float = Field(..., gt=0)
    width: float = Field(..., gt=0)


class CoilSchema(CoilAddSchema):
    id: int
    creation_date: datetime
    deletion_date: datetime | None
