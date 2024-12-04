from core.models.report.ResultModel import Result
from typing import TypeVar
from datetime import datetime, timedelta
from core.entities.CollectionEnumModel import Collections
from database.AggregationMethod import runAggregation

T = TypeVar("T")

def ARRByIndustryFilteration(filterData: T) -> Result:
    try:

        year = int(filterData.Year)

        column = filterData.ColumnName

        monthName = filterData.Month

        industryName = filterData.ColumnValue
        
        # Prepare date ranges for multiple months
        date_ranges = []
        for monthName in monthName:
            month = datetime.strptime(monthName, "%B").month
            start_date = datetime(year, month, 1)
            if month == 12:  # Handle December rollover
                end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
            else:
                end_date = datetime(year, month + 1, 1) - timedelta(days=1)
            date_ranges.append({"start_date": start_date, "end_date": end_date})

        pipelineQuery = {}
        if column.lower() == "Industry".lower():
            pipelineQuery = {f"CompanyDetails.{column}.Name": industryName}

        elif column.lower() == "LeadSource".lower():
            pipelineQuery = {f"{column}.Name": industryName}

        elif column.lower() == "AccountExecutiveName".lower():
            pipelineQuery = {f"{column}.Name": industryName}

        elif column.lower() == "Region".lower():
            industryName = filterData.ColumnValue.replace("/", " - ")
            pipelineQuery = {
                "BasicDealDetails.Type.Name": "Newbusiness",
                f"CompanyDetails.{column}.Name": industryName
            }
        else:
            pipelineQuery = {}

        Pipeline = [
            {
                # Convert CreateDate to date format if it's a string
                "$addFields": {
                    "convertedDate": {
                        "$cond": {
                            "if": {
                                "$eq": [
                                    {"$type": "$BasicDealDetails.CloseDate"},
                                    "string",
                                ]
                            },
                            "then": {
                                "$dateFromString": {
                                    "dateString": "$BasicDealDetails.CloseDate",
                                    "format": "%Y-%m-%d",
                                }
                            },
                            "else": "$BasicDealDetails.CloseDate",
                        }
                    }
                }
            },
            {
                "$match": {
                    "$and": [
                        {"BasicDealDetails.Stage.Name": "Closed Won"},
                        {**pipelineQuery},
                        {
                            "$or": [
                                {
                                    "convertedDate": {
                                        "$gte": date_range["start_date"],
                                        "$lt": date_range["end_date"],
                                    }
                                }
                                for date_range in date_ranges
                            ]
                        },
                    ]
                }
            },
            {
                # Group by RecordID and project fields in one stage
                "$group": {
                    "_id": "$BasicDealDetails.RecordID",
                    "DealName": {"$first": "$BasicDealDetails.Name"},
                    "DealAmount": {"$first": "$BasicDealDetails.Amount.Value"},
                    "DealType": {"$first": "$BasicDealDetails.Type.Name"},
                    "Region": {"$first": "$CompanyDetails.Region.Name"},
                    "Stage": {"$first": "$BasicDealDetails.Stage.Name"},
                    "Industry": {"$first": "$CompanyDetails.Industry.Name"},
                    "LeadSource": {"$first": "$LeadSource.Name"},
                    "CreateDate": {"$first": "$convertedDate"},
                }
            },
        ]

        Deals = runAggregation(Collections.Deals.value, Pipeline)

        return Result(Data=Deals, Status=1, Message="Done")

    except Exception as ex:
        message = f"Error occur at filterData: {ex}"
        return Result(Status=0, Message=message)
