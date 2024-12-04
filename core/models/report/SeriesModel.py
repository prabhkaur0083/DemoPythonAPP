from typing import List
from pydantic import BaseModel


class Series(BaseModel):
    Xaxis: List[str]
    Yaxis: List[float]
