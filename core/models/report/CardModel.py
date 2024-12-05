from pydantic import BaseModel
from core.models.report.SeriesModel import Series
from typing import Optional,List


class CardVisual(BaseModel):
    Title: str
    Content: str
    DyamicValue: Optional[str] = None
    DynamicVariance: Optional[str] = None
    DynamicTitle: Optional[str] = None
    DynamicColor: Optional[str] = None
    visualId: str
    SeriesData : Optional[List[Series]] = None
