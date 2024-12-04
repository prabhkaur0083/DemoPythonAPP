from pydantic import BaseModel, Field
from typing import Optional
from utils.GenerateRandomNumber import generateRandomNumber
from pytz import timezone
from datetime import datetime


class UserCredentials(BaseModel):
    Id: int = Field(default_factory=generateRandomNumber, alias="_id")

    UserId: int

    Token: str

    CreationTime: datetime

    ExpiredTime: datetime

    IsValid : Optional[bool] = True

    CreatedOn: datetime = datetime.now(timezone("Asia/Kolkata")).strftime(
        "%Y-%m-%d %H:%M:%S.%f"
    )

    CreatedBy: Optional[int] = 98765432

    UpdatedOn: datetime = datetime.now(timezone("Asia/Kolkata")).strftime(
        "%Y-%m-%d %H:%M:%S.%f"
    )

    UpdatedBy: Optional[int] = 98765432
