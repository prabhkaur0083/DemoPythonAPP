from pydantic import BaseModel
from typing import List
from typing import Optional


class FilterOptions(BaseModel):
    SlicerId: str
    SlicerValue: List[str]
