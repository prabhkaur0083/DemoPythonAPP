from pydantic import BaseModel, Field
from typing import Optional
from utils.GenerateRandomNumber import generateRandomNumber
from datetime import datetime
from pytz import timezone


class User(BaseModel):
    Id: Optional[int] = Field(default_factory=generateRandomNumber, alias="_id")

    FirstName: str

    LastName: str

    Email: str

    Password: str

    LastLogin: Optional[datetime] = None

    isActive: Optional[bool] = True

    isDeleted: Optional[bool] = False

    CreatedOn: datetime = datetime.now(timezone("Asia/Kolkata")).strftime(
        "%Y-%m-%d %H:%M:%S.%f"
    )

    CreatedBy: Optional[int] = 98765432

    UpdatedOn: datetime = datetime.now(timezone("Asia/Kolkata")).strftime(
        "%Y-%m-%d %H:%M:%S.%f"
    )

    UpdatedBy: Optional[int] = 98765432
