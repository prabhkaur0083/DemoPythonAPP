from core.models.report.ResultModel import Result
from datetime import datetime

def tokenVerification(verifiedResponse : Result) -> Result:
    try:
        if verifiedResponse.Status != 1 :

            return Result(Status=0, Message="Token Verification Failed,Token is Missing, Invalid or Expired.")

        return Result(Status=1, Message="Token Verified Successfully")
    
    except Exception as ex:
        message = f"Error occur at tokenVerification: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
