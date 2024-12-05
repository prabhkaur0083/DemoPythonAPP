import requests
from datetime import datetime
from core.models.report.ResultModel import Result
from constant.Constant import embedTokenURL
from  utils.RedisConnection import redisClient
from utils.convertTimeInSeconds import convertTimeIntoSeconds
from utils.SaveEmbedToken import saveTokenToFile

# Generate Embed Token
def generateEmbedToken(report_id, access_token, datasetID) -> Result:
    try:

        url = embedTokenURL
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        payload = {
            "datasets": [{"id": f"{datasetID}"}],
            "reports": [{"allowEdit": True, "id": f"{report_id}"}],
        }

        response = requests.post(url, json=payload, headers=headers)

        # Store the token with expiration in Redis
        # redis_key = "embedToken"  # Use tokenId for a unique key

        ttlSeconds = convertTimeIntoSeconds(response.json()["expiration"])

        # redisClient.setex(redis_key, ttlSeconds, response.json()["token"])
        
        embedtoken = response.json()["token"]

        saveTokenToFile(embedtoken, ttlSeconds)

        return Result(
            Data=embedtoken, Status=1, Message="Embed token successfully created"
        )
    except Exception as ex:
        message = f"Error occur at generateEmbedToken: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
