from datetime import datetime
from services.report.GetEmbedToken import generateEmbedToken
from services.report.GetAccessToken import generateAccessToken
from services.report.PowerbiJs import visualExtraction
from core.models.report.ResultModel import Result
# from configurations.tokens import embedToken
from utils.ReadEmbedToken import readTokenFromFile
from utils.RedisConnection import redisClient
import time
from services.report.ExtractReportDatasetID import extractReportDatasetId

# Extract Visual Data
def extractVisualData(workspaceId, reportId, pagename, slicerOptions=[]) -> Result:
    try:

        tokenData = readTokenFromFile()

        current_time = time.time()

        print(current_time)

        expiration_time = tokenData["timestamp"] + tokenData["expiration"]

        if current_time >= expiration_time :

            print("new One")
        # embedToken = redisClient.get("embedToken")

            accessToken = generateAccessToken()

            if accessToken.Status != 1:
                return accessToken

            datasetId = extractReportDatasetId(workspaceId, reportId, accessToken.Data)

            if datasetId.Status != 1:
                return datasetId

            tokenResult = generateEmbedToken(reportId, accessToken.Data, datasetId.Data)

            if tokenResult.Status != 1:
                return tokenResult
            
            embedToken = tokenResult.Data
        else :
            print("exiting")
            embedToken =  tokenData["token"]
        

        return visualExtraction(
            embedToken, reportId, workspaceId, pagename, slicerOptions
        )
    
    except Exception as ex:
        message = f"Error occur at extractVisualData: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
