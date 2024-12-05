from datetime import datetime
from services.report.GetEmbedToken import generateEmbedToken
from services.report.GetAccessToken import generateAccessToken
from services.report.PowerbiJs import visualExtraction
from core.models.report.ResultModel import Result
from configurations.tokens import embedToken
from utils.RedisConnection import redisClient
from services.report.ExtractReportDatasetID import extractReportDatasetId

# Extract Visual Data
def extractVisualData(workspaceId, reportId, pagename, slicerOptions=[]) -> Result:
    try:

        embedToken = redisClient.get("embedToken")

        if not embedToken:
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

        return visualExtraction(
            embedToken, reportId, workspaceId, pagename, slicerOptions
        )
    
    except Exception as ex:
        message = f"Error occur at extractVisualData: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
