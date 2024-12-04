from pydantic import BaseModel
from typing import List
from typing import Optional


class FilterBody(BaseModel):
    Year: str
    Month: List[str]
    Region: Optional[str] = None
    ColumnName: Optional[str] = None
    ColumnValue: Optional[str]= None
