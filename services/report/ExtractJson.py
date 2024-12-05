from core.models.report.ResultModel import Result
import json
import os
import datetime


def extractJsonData(fileName:str) -> Result:
    try:
        folderName = "PagesJsons"
        file_path = os.path.join(folderName, fileName)
        with open(file_path, "r") as f:
            content = json.load(f)
        return Result(
            Data=content["Data"], Status=1, Message="Json Data Loaded Successfully"
        )
    except Exception as ex:
        message = f"Error occur at extractVisualData: {ex}"
        print(f"{datetime.datetime.now()} {message}")
        return Result(Status=0, Message=message)
