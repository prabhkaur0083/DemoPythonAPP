import json
from datetime import datetime
from utils.MillionConversion import millionConversion
from utils.ThousandConversion import thousandsConversion
from core.models.report.ResultModel import Result


def cardsFormattingViaTable(table) -> Result:
    try:
        if isinstance(table, str):
            table = json.loads(table)
        columns = table["Columns"]
        rows = table["Rows"]

        allCardsData = []

        # Process each row in the table
        for row in rows:
            # Initialize variables for CardVisual attributes
            cardData = {
                "Title": "",
                "Content": "",
                "DyamicValue": "",
                "DynamicVariance": "",
                "ContentColor": "",
                "DynamicTitle": "",
            }

            unit = row[6]

            for i, col in enumerate(columns):
                if "header" in col.lower():
                    cardData["Title"] = row[i]

                elif "unit" in col.lower():
                    unit = row[i]

                elif (
                    "_SaaSMetric_CM" in col
                    or "_cm val" in col.lower()
                    or "_cohortData_CM" in col
                ):
                    if row[0] == "ARR":
                        try:
                            if float(row[i]) >= 1000000:
                                cardData["Content"] = millionConversion(row[i], unit)
                            else:
                                cardData["Content"] = thousandsConversion(row[i], unit)
                        except:
                            cardData["Content"] = row[i]

                    elif row[0].lower() in [
                        "new bookings",
                        "expansions",
                        "mrr",
                        "avgacv/arpu",
                        "customer lifetime value (clv)",
                        "customer acquisition cost (cac)",
                        "open pipeline",
                        "avg. deal size"
                    ]:
                        cardData["Content"] = thousandsConversion(row[i], unit)
                    else:
                        if unit == "#":
                            unit = ""

                        try:
                            if unit == "%":
                                # Check if the value is a float
                                value = float(row[i]) * 100
                                if value.is_integer():  # If the value is an integer
                                    cardData["Content"] = f"{int(value)}{unit}"
                                else:  # If the value is a float
                                    cardData["Content"] = f"{value:.2f}{unit}"
                            else:
                                # Check if the value is a float
                                value = float(row[i])
                                if value.is_integer():  # If the value is an integer
                                    cardData["Content"] = f"{unit}{int(value)}"
                                else:  # If the value is a float
                                    cardData["Content"] = f"{unit}{value:.2f}"
                        except:
                            cardData["Content"] = f"{row[i]}{unit}"

                elif (
                    "dynamic val" in col.lower()
                    or "_SaaSMetric_PM" == col
                    or "_cohortData_PM" == col
                ):
                    if row[0] == "ARR":
                        cardData["DyamicValue"] = millionConversion(row[i], unit)
                    elif row[0].lower() in [
                        "new bookings",
                        "expansions",
                        "mrr",
                        "avgacv/arpu",
                        "customer lifetime value (clv)",
                        "customer acquisition cost (cac)",
                        "open pipeline",
                        "avg. deal size"
                    ]:
                        cardData["DyamicValue"] = thousandsConversion(row[i], unit)
                    else:
                        if unit == "#":
                            unit = ""

                        try:
                            if unit == "%":
                                # Check if the value is a float
                                value = float(row[i]) * 100
                                if value.is_integer():  # If the value is an integer
                                    cardData["DyamicValue"] = f"{int(value)}{unit}"
                                else:  # If the value is a float
                                    cardData["DyamicValue"] = f"{value:.2f}{unit}"
                            else:
                                # Check if the value is a float
                                value = float(row[i])
                                if value.is_integer():  # If the value is an integer
                                    cardData["DyamicValue"] = f"{unit}{int(value)}"
                                else:  # If the value is a float
                                    cardData["DyamicValue"] = f"{unit}{value:.2f}"
                        except:
                            cardData["DyamicValue"] = f"{row[i]}{unit}"

                elif (
                    ("variance" in col.lower() and "cf" not in col.lower())
                    or "_SaaSMetric_Var" == col
                    or "_cohortData_Var" == col
                ):
                    cardData["DynamicVariance"] = row[i]

                elif (
                    "variancecf" in col.lower()
                    or "_SaaSMetric_VarCF" in col
                    or "_cohortData_VarCF" in col
                ):
                    cardData["ContentColor"] = row[i]

                elif "title" in col.lower():
                    cardData["DynamicTitle"] = row[i]
            for key in cardData:
                if not cardData[key] or cardData[key] == "%" or cardData[key] == "$":
                    cardData[key] = "--"

            # Append the card data to the all_card_data list
            allCardsData.append(cardData)

        return Result(Data=allCardsData, Status=1, Message="Data formatted")

    except Exception as ex:
        message = f"Error occur at cardsFormatting: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
