from pydantic import BaseModel
from typing import List
from core.models.report.FilterOptionsModel import FilterOptions


class VisualRequestBody(BaseModel):
    workspaceId: str
    reportId: str
    pagename: str
    filters: List[FilterOptions]
