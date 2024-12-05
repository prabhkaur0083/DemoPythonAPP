import requests
from core.models.report.ResultModel import Result
from datetime import datetime


def extractReportDatasetId(workSpaceID, reportId, accessToken) -> Result:
    try:
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{workSpaceID}/reports/{reportId}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {accessToken}",
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            datasetId = response.json()["datasetId"]
            return Result(
                Data=datasetId, Status=1, Message="Dataset ID retrived successfully"
            )
        else:
            return Result(
                Status=0,
                Message="Invalid Report ID or WorkSpaceId, please Check your Data",
            )
    except Exception as ex:
        message = f"Error occur at extractReportDatasetId: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
