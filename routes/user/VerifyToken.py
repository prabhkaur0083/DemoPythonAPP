from fastapi import APIRouter, Depends
from core.models.report.ResultModel import Result
from services.user.TokenVerify import tokenVerification
from utils.TokenVerification import verifyToken

TokenVerifyRouter = APIRouter()


@TokenVerifyRouter.post("/verify/")
def verifyTokenData(verifiedResponse: dict = Depends(verifyToken)) -> Result:
    
    return tokenVerification(verifiedResponse)
