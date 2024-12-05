from fastapi import APIRouter
from core.models.report.ResultModel import Result
from core.entities.CollectionEnumModel import Collections
from services.user.DeleteUserToken import deleteUserCredentials
from core.models.user.TokenRequestBody import TokenRequest

DeleteTokenRouter = APIRouter()


@DeleteTokenRouter.post("/delete")
def deleteToken(token: TokenRequest) -> Result:
    return deleteUserCredentials(token, Collections.UserCredentials.value)
