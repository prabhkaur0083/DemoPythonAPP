from typing import Optional, List
from pydantic import BaseModel
from core.models.report.CardModel import CardVisual
from core.models.report.ChartsModel import ChartVisual
from core.models.report.TableModel import TableVisual
from core.models.report.SlicerModel import SlicerVisual
from core.models.report.FIlterValuesModel import FilterValues


class Response(BaseModel):
    Cards: Optional[List[CardVisual]] = []
    Charts: Optional[List[ChartVisual]] = []
    Tables: Optional[List[TableVisual]] = []
    Slicer: Optional[List[SlicerVisual]] = []
    AdvancedSlicer: Optional[List[SlicerVisual]] = []
    FilterValues: Optional[List[FilterValues]]
