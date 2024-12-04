import requests
from datetime import datetime
from core.models.report.ResultModel import Result
from constant.Constant import accessTokenURL
from configurations.DataConfig import BaseConfig


# Generate Access Token
def generateAccessToken() -> Result:
    try:
        url = accessTokenURL.format(tenant_id=BaseConfig.TENANT_ID)
        payload = {
            "grant_type": "client_credentials",
            "client_id": BaseConfig.CLIENT_ID,
            "client_secret": BaseConfig.CLIENT_SECRET,
            "scope": "https://analysis.windows.net/powerbi/api/.default",
        }
        response = requests.post(url, data=payload)
        accessToken = response.json()["access_token"]
        return Result(
            Data=accessToken, Status=1, Message="Access token successfully created"
        )
    except Exception as ex:
        message = f"Error occur at generateAccessToken: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
