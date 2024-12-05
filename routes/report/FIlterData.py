from fastapi import APIRouter
from core.models.report.ResultModel import Result
from services.report.NewBookingChartDrilling import newBookingsFilteration
from services.report.ARRbyIndustryChartDrilling import ARRByIndustryFilteration
from core.models.report.FilterRequestBody import FilterBody


DataFilterRouter = APIRouter()


@DataFilterRouter.post("/NewBookingsChart/get")
def getNewBookingsDrilldown(filterBody: FilterBody) -> Result:
    return newBookingsFilteration(filterBody)

@DataFilterRouter.post("/IndustryARR/get")
def getIndustryARRDrilldown(filterBody: FilterBody) -> Result:
    return ARRByIndustryFilteration(filterBody)
