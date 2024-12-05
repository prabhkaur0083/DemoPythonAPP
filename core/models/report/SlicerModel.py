from typing import List, Optional
from pydantic import BaseModel


class SlicerVisual(BaseModel):
    Id: str
    Title: str
    Options: List[str]
    TableName: str
    ColumnName: str
    SelectedValues: Optional[List[str]] = None
    visualId: str
