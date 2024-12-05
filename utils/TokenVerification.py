from fastapi import Header
from database.CRUD import MongoDBHandler
from core.entities.CollectionEnumModel import Collections
from datetime import datetime
from core.models.report.ResultModel import Result

def verifyToken(authorization: str = Header(None))->Result:
    try : 
        if not authorization:
            return Result(Status=0, Message="Authorization header missing")

        # Extract the token (assuming "Bearer <token>")
        token = authorization.split(" ")[1] if " " in authorization else authorization

        # Fetch token details from the database
        mongoDb = MongoDBHandler()

        tokenData = mongoDb.findDocument(
            Collections.UserCredentials.value, {"Token": token}
        )

        if not tokenData.Data:
            return Result(Status=0, Message="Invalid token")

        # Check expiration
        expire_time = tokenData.Data.get("ExpiredTime")

        # Check if the expiration time exists and is valid
        if expire_time is None:
            return Result(
                Status=0, Message="Token does not contain an expiration time"
            )

        # Ensure expire_time is a datetime object before comparison
        if isinstance(expire_time, str):
            # If expire_time is a string, convert it to a datetime object
            expire_time = datetime.fromisoformat(expire_time)

        # Check expiration
        if datetime.now() > expire_time:
            mongoDb.deleteDocument(
                Collections.UserCredentials.value, {"Token": token}
            )
            return Result(Status=401, Message="Token has expired")

        return Result(Status=1, Message="Token Verified SuccessFully")
    
    except Exception as ex:
        message = f"Error occur at verifyToken: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
