from core.models.report.ResultModel import Result
from datetime import datetime, timedelta
from typing import TypeVar
from core.entities.CollectionEnumModel import Collections
from utils.GenerateRandomString import generateRandomString
from database.CRUD import MongoDBHandler
from utils.HashedPassword import verifyPassword
from core.entities.user.UserCredentials import UserCredentials

T = TypeVar("T")


def userLogin(loginData: T, collection: str) -> Result:
    try:
        mongoDb = MongoDBHandler()

        # Retrieve the user document by email
        existingUser = mongoDb.findDocument(collection, {"Email": loginData.Email})

        # Check if the user exists
        if existingUser.Data:
            stored_password_hash = existingUser.Data["Password"]

            # Use the verifyPassword function to check if the password matches
            if verifyPassword(stored_password_hash, loginData.Password):
                # If the password matches, proceed with creating the session/token
                creation_time = datetime.now()
                expire_time = creation_time + timedelta(minutes=480)

                # Create UserCredentials object with the required fields
                userCredentials = UserCredentials(
                    UserId=existingUser.Data.get("_id"),
                    Token=generateRandomString(),
                    CreationTime=creation_time,
                    ExpiredTime=expire_time,
                )
                result = mongoDb.insertDocument(
                    Collections.UserCredentials.value,
                    userCredentials.dict(by_alias=True),
                )
                return Result(Data=result.Data, Status=1, Message="Login Successfully")

            # If password does not match
            return Result(
                Status=0, Message="Invalid Credentials, Please Check Your Credentials"
            )

        # If user does not exist
        return Result(
            Status=0, Message="Invalid Credentials, Please Check Your Credentials"
        )

    except Exception as ex:
        message = f"Error occur at userLogin: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)