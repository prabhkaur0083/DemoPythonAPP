from fastapi import APIRouter
from core.models.user.LoginRequestModel import LoginRequest
from core.models.report.ResultModel import Result
from core.entities.CollectionEnumModel import Collections
from services.user.UserLogin import userLogin

LoginRouter = APIRouter()


@LoginRouter.post("/login")
def loginUser(requestBody: LoginRequest) -> Result:
    
    return userLogin(requestBody, Collections.User.value)
