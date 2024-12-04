from fastapi import APIRouter
from core.models.report.ResultModel import Result
from services.report.ExtractJson import extractJsonData

VisualJsonRouter = APIRouter()


@VisualJsonRouter.get("/{filepath}/get")
def getJsonVisual(filepath: str) -> Result:
    return extractJsonData(filepath)
