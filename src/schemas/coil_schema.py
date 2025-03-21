from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class CoilAddSchema(BaseModel):
    length: float = Field(..., gt=0)
    weight: float = Field(..., gt=0)


class CoilSchema(CoilAddSchema):
    id: int
    creation_date: datetime
    deletion_date: datetime | None


class CoilFilterSchema(BaseModel):
    id_min: Optional[int] = Field(None, gt=0)
    id_max: Optional[int] = Field(None, gt=0)
    length_min: Optional[float] = Field(None, gt=0)
    length_max: Optional[float] = Field(None, gt=0)
    weight_min: Optional[float] = Field(None, gt=0)
    weight_max: Optional[float] = Field(None, gt=0)
    creation_date_min: Optional[datetime] = Field(None)
    creation_date_max: Optional[datetime] = Field(None)
    deletion_date_min: Optional[datetime] = Field(None)
    deletion_date_max: Optional[datetime] = Field(None)
