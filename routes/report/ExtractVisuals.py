from fastapi import APIRouter
from core.models.report.ResultModel import Result
from services.report.ExtractVisualdata import extractVisualData
from core.models.report.VisualRequestBodyModel import VisualRequestBody

VisualRouter = APIRouter()


@VisualRouter.post("/get")
def getVisual(requestData: VisualRequestBody) -> Result:
    # Get Parameters Values
    workspaceId = requestData.workspaceId
    reportId = requestData.reportId
    pagename = requestData.pagename
    options = requestData.filters
    return extractVisualData(workspaceId, reportId, pagename, options)











# # Extract Report Visual BY PowerBi Reports
# @app.get(
#     "/api/v1/report/visual/{workspaceId}/{reportId}/{pagename}", response_model=Result
# )
# def getVisualData(workspaceId: str, reportId: str, pagename: str) -> Result:
#     return extractVisualData(workspaceId, reportId, pagename)
