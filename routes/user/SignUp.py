from fastapi import APIRouter
from core.entities.user.UserModel import User
from core.models.report.ResultModel import Result
from core.entities.CollectionEnumModel import Collections
from services.user.UserSignup import userSignUp

SignUpRouter = APIRouter()


@SignUpRouter.post("/create/")
def createUser(requestBody: User) -> Result:
    return userSignUp(requestBody, Collections.User.value)
