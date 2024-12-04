from core.models.report.ResultModel import Result
from datetime import datetime
from typing import TypeVar
from database.CRUD import MongoDBHandler
from utils.HashedPassword import passwordHashing

T = TypeVar("T")


def userSignUp(userData: T, collection: str) -> Result:
    try:

        mongoDb = MongoDBHandler()

        # Check if the email already exists in the database
        existingUser = mongoDb.findDocument(collection, {"Email": userData.Email})

        if existingUser.Data:
            return Result(Status=400, Message="User Already Exist")
        
        userPassword = userData.Password

        # Convert the model to a dictionary and insert it into MongoDB
        userDict = userData.dict(by_alias=True)

        userDict["Password"] = passwordHashing(userPassword)

        result = mongoDb.insertDocument(collection, userDict)

        if result.Status == 2:
            userSignUp(userData)

        return Result(Data=result.Data, Status=1, Message="User Created Successfully")

    except Exception as ex:
        message = f"Error occur at extractVisualData: {ex}"
        print(f"{datetime.datetime.now()} {message}")
        return Result(Status=0, Message=message)
