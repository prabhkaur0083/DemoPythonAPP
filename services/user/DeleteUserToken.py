from datetime import datetime
from database.CRUD import MongoDBHandler
from core.models.report.ResultModel import Result


def deleteUserCredentials(token: str, collection : str) -> Result:
    try:
        # Initialize MongoDB handler
        mongoDb = MongoDBHandler()

        tokenString = token.dict()["token"]

        # Check if the token exists in the database
        credentialData = mongoDb.findDocument(collection, {"Token": tokenString})

        if not credentialData.Data:
            return Result(Status=404, Message="Token not found")

        # Delete the user credentials document
        result = mongoDb.deleteDocument(collection, {"Token": tokenString})

        if result.Status == 1:  # If deletion was successful
            return Result(Status=1, Message="User credentials deleted successfully")

    except Exception as ex:
        message = f"Error occur at deleteUserCredentials: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
