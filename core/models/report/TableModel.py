from typing import List
from pydantic import BaseModel
from typing import Optional


class TableVisual(BaseModel):
    Type: str
    Title: str
    Unit: Optional[str]
    Columns: List[str]
    Rows: List[List[str]]
    visualId: str
