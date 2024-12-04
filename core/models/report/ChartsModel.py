from typing import List
from pydantic import BaseModel
from typing import Optional
from core.models.report.SeriesModel import Series


class ChartVisual(BaseModel):
    Type: str
    Title: str
    Unit: Optional[str]
    SeriesData: List[Series]
    visualId: str
