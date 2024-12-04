from pydantic import BaseModel
from typing import List, Optional


class FilterValues(BaseModel):
    Year: List
    Month: List
    Region: Optional[List] = None
    Comparison: Optional[List]
