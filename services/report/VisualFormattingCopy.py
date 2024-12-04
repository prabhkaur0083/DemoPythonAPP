from typing import List
from datetime import datetime
import re
from core.models.report.CardModel import CardVisual
from core.models.report.ChartsModel import ChartVisual
from core.models.report.TableModel import TableVisual
from core.models.report.SlicerModel import SlicerVisual
from core.models.report.SeriesModel import Series
from core.models.report.ResponseModel import Response
from core.models.report.ResultModel import Result
from utils.MillionConversion import millionConversion
from utils.ThousandConversion import thousandsConversion
from utils.ExtractCardContent import extractCardContent


def formatData(visualdata) -> Result:
    try:
        visuals = visualdata["data"]

        cards: List[CardVisual] = []
        charts: List[ChartVisual] = []
        tables: List[TableVisual] = []
        series: List[Series] = []
        slicers: List[SlicerVisual] = []
        advancedSlicer: List[SlicerVisual] = []
        i = 1

        # tempory Value Store Variables
        cardTitle = ""
        cardContent = ""
        cardDynamicValue = ""
        cardComparisonValue = ""
        cardDynamiVariance = ""
        netBlendedValue = ""
        for visual in visuals:
            title = visual["Title"]

            if "card" in visual["Type"].lower():
                content = visual["VisualData"]["data"]

                if title == "Net Blended ACV":
                    netBlendedValue = extractCardContent(content)
                    print(netBlendedValue)
                    continue

                if "Dynamic" not in title and "-" not in title:
                    cardTitle = title

                if title == f"{cardTitle}":
                    print(title, cardTitle, "-***********-")
                    formatCardContent = extractCardContent(content)
                    if any(keyword in title for keyword in ["ARR"]):
                        cardContent = millionConversion(formatCardContent)
                    elif any(
                        keyword in title
                        for keyword in [
                            "MRR",
                            "New Bookings",
                            "Expansions",
                            "Expansion",
                            "Avg. ACV/ARPU",
                        ]
                    ):
                        cardContent = thousandsConversion(formatCardContent)
                    else:
                        cardContent = formatCardContent
                    print(cardContent, "hfjdhffffffffffffj")
                    continue

                if title == f"{cardTitle}-PM":
                    formatComparisonValue = extractCardContent(content)
                    if any(keyword in title for keyword in ["ARR"]):
                        cardComparisonValue = millionConversion(formatComparisonValue)
                    elif any(
                        keyword in title
                        for keyword in [
                            "MRR",
                            "New Bookings",
                            "Expansions",
                            "Avg. ACV/ARPU",
                        ]
                    ):
                        cardComparisonValue = thousandsConversion(formatComparisonValue)
                    else:
                        cardComparisonValue = formatComparisonValue
                    continue

                if title == f"Dynamic {cardTitle}":
                    try:
                        cardValue = extractCardContent(content)
                        if title == "Dynamic ARR" or title == "ARR":
                            dynamicValue = millionConversion(cardValue)
                        elif any(
                            keyword in title
                            for keyword in [
                                "MRR",
                                "New Bookings",
                                "Expansions",
                                "Avg. ACV/ARPU",
                            ]
                        ):
                            dynamicValue = thousandsConversion(cardValue)
                        else:
                            dynamicValue = cardValue
                        cardDynamicValue = f"{dynamicValue}"
                    except:
                        dynamicValue = "--"

                    continue

                if title == f"Dynamic {cardTitle} Variance":
                    cardDynamiVariance = extractCardContent(content)

                print(cardContent, "-------")
                cards.append(
                    CardVisual(
                        Title=cardTitle,
                        Content=cardContent,
                        ComparisonValue=cardComparisonValue,
                        DyamicValue=cardDynamicValue,
                        DynamicVariance=cardDynamiVariance,
                        NetBlendedValue=netBlendedValue,
                        visualId=f"visual{i}",
                    )
                )

            if "chart" in visual["Type"].lower() or visual["Type"] == "funnel":
                dataUnit = ""
                chartcontent = visual["VisualData"]["data"]
                lines = chartcontent.strip().split("\r\n")
                series: List[Series] = []

                # Assuming the first line is headers and subsequent lines are data
                headers = lines[0].split(",")

                data_lines = lines[1:]

                # Create Series data for each metric column
                for col_index in range(1, len(headers)):
                    x_axis = []
                    y_axis = []
                    for line in data_lines:
                        parts = line.split(",")
                        x_value = parts[0].strip()  # Month
                        y_value = parts[col_index].strip()  # Metric value
                        try:
                            print(y_value)

                            unit = y_value[0][0]
                            # Attempt to convert y_value to a float, removing any non-numeric characters
                            numeric_value = float(re.sub(r"[^\d.-]", "", y_value))
                            x_axis.append(x_value)  # Append the x_value (e.g., month)
                            y_axis.append(numeric_value)  # Append the numeric y_value
                        except:
                            # print("No chart")
                            try:
                                print(x_value)
                                unit = x_value[0][0]
                                numeric_value = float(re.sub(r"[^\d.-]", "", x_value))
                                x_axis.append(
                                    y_value
                                )  # Append the x_value (e.g., month)
                                y_axis.append(numeric_value)

                            # # If both fail, skip this line or handle it differently as needed
                            except:
                                continue

                    series.append(Series(Xaxis=x_axis, Yaxis=y_axis))
                if unit.isnumeric():
                    dataUnit = ""
                else:
                    dataUnit = unit

                charts.append(
                    ChartVisual(
                        Type=visual["Type"],
                        Title=title,
                        Unit=dataUnit,
                        SeriesData=series,
                        visualId=f"visual{i}",
                    )
                )
            if visual["Type"] == "tableEx":
                dataUnit = ""
                tableContent = visual["VisualData"]["data"]
                lines = tableContent.split("\n")
                columns = lines[0].split(",")

                rows = [
                    line.split(",") for line in lines[1:] if line
                ]  # Remove empty lines
                cleaned_rows = [
                    [cell.replace("\r", "").replace('"', "") for cell in row]
                    for row in rows
                ]

                tables.append(
                    TableVisual(
                        Type=visual["Type"],
                        Unit=dataUnit,
                        Title=title,
                        Columns=columns,
                        Rows=cleaned_rows,
                        visualId=f"visual{i}",
                    )
                )

            if visual["Type"] == "pivotTable":
                tableContent = visual["VisualData"]["data"]
                lines = tableContent.split("\n")
                columns = lines[0].split(",")

                rows = [
                    line.split(",") for line in lines[1:] if line
                ]  # Remove empty lines
                data = rows[1][1]
                if data.isdigit():
                    dataUnit = ""
                else:
                    dataUnit = data[0]
                cleaned_rows = [
                    [
                        cell.replace("\r", "").replace('"', "").replace(dataUnit, "")
                        for cell in row
                    ]
                    for row in rows
                ]

                tables.append(
                    TableVisual(
                        Type=visual["Type"],
                        Unit=dataUnit,
                        Title=title,
                        Columns=columns,
                        Rows=cleaned_rows,
                        visualId=f"visual{i}",
                    )
                )

            if visual["Type"] == "slicer":
                slicerId = visual["Id"]
                tableName = visual["TableName"]
                columnName = visual["ColumnName"]
                slicerContent = visual["VisualData"]["data"]
                slicerList = slicerContent.split("\r\n")[1:]
                slicers.append(
                    SlicerVisual(
                        Id=slicerId,
                        Title=title,
                        Options=slicerList,
                        TableName=tableName,
                        ColumnName=columnName,
                        visualId=f"visual{i}",
                    )
                )

            if visual["Type"] == "advancedSlicerVisual":
                slicerId = visual["Id"]
                tableName = visual["TableName"]
                columnName = visual["ColumnName"]
                slicerContent = visual["VisualData"]["data"]
                slicerList = slicerContent.split("\r\n")[1:]
                advancedSlicer.append(
                    SlicerVisual(
                        Id=slicerId,
                        Title=title,
                        TableName=tableName,
                        ColumnName=columnName,
                        Options=slicerList,
                        visualId=f"visual{i}",
                    )
                )

            i = i + 1
            # if visual["Type"] == "advancedSlicerVisual":
            #     slicerId = visual["Id"]
            #     slicerContent = visual["VisualData"]["data"]
            #     slicerList = slicerContent.split("\r\n")[1:]
            #     advancedSlicer.append(SlicerVisual(Id=slicerId,Title=title, Options=slicerList,visualId = f"visual{i}"))
            # i=i+1
        Data = Response(
            Cards=cards,
            Charts=charts,
            Tables=tables,
            Slicer=slicers,
            AdvancedSlicer=advancedSlicer,
        )
        json_data = Data.json()

        # Save the JSON data to a file
        with open("page1.json", "w") as f:
            f.write(json_data)

        print("Data saved to data.json")
        return Result(
            Data=Response(
                Cards=cards,
                Charts=charts,
                Tables=tables,
                Slicer=slicers,
                AdvancedSlicer=advancedSlicer,
            ),
            Status=1,
            Message="Success",
        )
    except Exception as ex:
        message = f"Error occur at formatData: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
