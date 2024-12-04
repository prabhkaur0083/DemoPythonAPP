from core.models.report.ResultModel import Result
from typing import TypeVar
from datetime import datetime,timedelta
from core.entities.CollectionEnumModel import Collections
from database.AggregationMethod import runAggregation

T = TypeVar("T")

def newBookingsFilteration(filterData: T) -> Result:
    try:
        year = int(filterData.Year)

        monthName = filterData.Month
        
        regionName = filterData.ColumnValue.replace("/"," - ")

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

        # Append logic for multiple months
        Pipeline = [
            {
                # Convert CreateDate to date format if it's a string
                "$addFields": {
                    "convertedDate": {
                        "$cond": {
                            "if": {
                                "$eq": [
                                    {"$type": "$BasicDealDetails.CreateDate"},
                                    "string",
                                ]
                            },
                            "then": {
                                "$dateFromString": {
                                    "dateString": "$BasicDealDetails.CreateDate",
                                    "format": "%Y-%m-%d",
                                }
                            },
                            "else": "$BasicDealDetails.CreateDate",
                        }
                    }
                }
            },
            {
                # Match logic for multiple date ranges with $or
                "$match": {
                    "$and": [
                        {"BasicDealDetails.Type.Name": "Newbusiness"},
                        {"CompanyDetails.Region.Name": regionName},
                        {"BasicDealDetails.Stage.Name": "Closed Won"},
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
