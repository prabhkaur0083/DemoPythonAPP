from core.models.report.ResultModel import Result
from datetime import datetime
from database.CRUD import MongoDBHandler


def runAggregation(collectionName: str, pipeline: list) -> Result:
    try:
        mongoObj = MongoDBHandler()
        collection = mongoObj.getCollection(collectionName)
        result = list(collection.aggregate(pipeline))

        if result:
            return Result(
                Data=result, Status=1, Message="Aggregation successfully completed"
            )

        else:
            return Result(Status=1, Message="No documents found for aggregation")

    except Exception as ex:
        message = f"Error while running aggregation in {collectionName}: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
