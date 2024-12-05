from typing import List
from datetime import datetime
from core.models.report.CardModel import CardVisual
from core.models.report.ChartsModel import ChartVisual
from core.models.report.TableModel import TableVisual
from core.models.report.SlicerModel import SlicerVisual
from core.models.report.SeriesModel import Series
from core.models.report.ResponseModel import Response
from core.models.report.ResultModel import Result
from core.models.report.FIlterValuesModel import FilterValues
from utils.TableDataFormatting import processTable
from utils.CardsFormattingViaTable import cardsFormattingViaTable
from utils.ChartDataFormatting import chartFormatting
from utils.CardsFormatting import cardFormatting 


def formatData(visualdata) -> Result:
    try:
        visuals = visualdata["data"]

        cards: List[CardVisual] = []
        charts: List[ChartVisual] = []
        tables: List[TableVisual] = []
        slicers: List[SlicerVisual] = []
        filters: List[FilterValues] = []
        advancedSlicer: List[SlicerVisual] = []

        cards_dict = {}

        i = 1
        for visual in visuals:
            title = visual["Title"]

            # Cards Formatting Via a Table

            if "card" in visual["Type"].lower():

                resultData = cardFormatting(visual)

                if resultData:

                    cardVisual = CardVisual(
                        Title=resultData["Title"],
                        Content=resultData["Content"],
                        DyamicValue=resultData["DyamicValue"],
                        DynamicVariance=resultData["DynamicVariance"],
                        DynamicTitle=resultData["DynamicTitle"],
                        DynamicColor=resultData["ContentColor"],
                        visualId=f"visual{i}",
                    )

                    cards_dict[resultData["Title"]] = cardVisual

                    # static To Handle specific Code (needs to be remove)
                    # Static logic to handle specific code (needs to be removed later)
                    if cards_dict.get("Open Pipeline#") and cards_dict.get("Open Pipeline"):
                        # Accessing Pydantic model attributes with dot notation
                        cards_dict.get("Open Pipeline").DynamicTitle = cards_dict.get("Open Pipeline#").Title
                        cards_dict.get("Open Pipeline").DyamicValue = cards_dict.get("Open Pipeline#").Content


                    cards.append(cardVisual)

            if "Cards Data Table".lower() in visual["Title"].lower() :
                
                formattedData = processTable(visual)
                result = formattedData.Data

                Table = TableVisual(
                    Type=visual["Type"],
                    Unit="",
                    Title=title,
                    Columns=result["Columns"],
                    Rows=result["Rows"],
                    visualId=f"visual{i}",
                )

                tableJson = Table.json()

                result = cardsFormattingViaTable(tableJson)

                # Extract formatted card data
                cardFormattedData = result.Data

                if cardFormattedData:
                    for cardData in cardFormattedData:
                        cardVisual = CardVisual(
                            Title=cardData["Title"],
                            Content=cardData["Content"],
                            DyamicValue=cardData["DyamicValue"],
                            DynamicVariance=cardData["DynamicVariance"],
                            DynamicTitle=cardData["DynamicTitle"],
                            DynamicColor=cardData["ContentColor"],
                            visualId=f"visual{i}",
                        )

                        # Create a card and store it in the dictionary
                        cards_dict[cardData["Title"]] = cardVisual

                        # Add the CardVisual instance to the list
                        cards.append(cardVisual)
                        i = i + 1
                else:
                    print("No formatted card data available.")

            # Chart Formatting 
            if (
                "chart" in visual["Type"].lower()
                or visual["Type"] == "funnel"
                or visual["Type"] == "PBI_CV_25997FEB_F466_44FA_B562_AC4063283C4C"
            ):
                card = cards_dict.get(visual["Title"])

                responseData = chartFormatting(visual)

                header_text = responseData.Data["headerTitle"][0]  # Get the header text
                card2 = None  

                # Iterate through the dictionary to find a key that contains the header text
                for key, value in cards_dict.items():
                    if header_text == "OpenPipeline#":
                        header_text = "Open Pipeline"

                    if key.lower() in header_text.lower() :  
                        card2 = value

                if card :
                    card.SeriesData = responseData.Data["seriesData"]
                elif card2:
                    print("yes")
                    card2.SeriesData = responseData.Data["seriesData"]
            
                else:
                    charts.append(
                        ChartVisual(
                            Type=visual["Type"],
                            Title=title,
                            Unit=responseData.Data["unit"],
                            SeriesData=responseData.Data["seriesData"],
                            visualId=f"visual{i}",
                        )
                    )

            # Table Formatting 
            if visual["Type"] == "tableEx" or visual["Type"] == "pivotTable":
                formattedData = processTable(visual)
                result = formattedData.Data

                Table = TableVisual(
                    Type=visual["Type"],
                    Unit="",
                    Title=title,
                    Columns=result["Columns"],
                    Rows=result["Rows"],
                    visualId=f"visual{i}",
                )

                tables.append(Table)

            # Slicer Formattting    
            if "slicer" in visual["Type"].lower():
                slicerId = visual["Id"]
                tableName = visual["TableName"]
                columnName = visual["ColumnName"]
                selectedValues = visual["selectedValue"]
                slicerContent = visual["VisualData"]["data"]
                slicerList = slicerContent.split("\r\n")[1:]
                slicers.append(
                    SlicerVisual(
                        Id=slicerId,
                        Title=title,
                        Options=slicerList,
                        TableName=tableName,
                        ColumnName=columnName,
                        SelectedValues=selectedValues,
                        visualId=f"visual{i}",
                    )
                )

            i = i + 1

        Data = Response(
            Cards=cards,
            Charts=charts,
            Tables=tables,
            Slicer=slicers,
            AdvancedSlicer=advancedSlicer,
            FilterValues=filters,
        )
        json_data = Data.json()

        # Save the JSON data to a file
        # with open("temporaryData/page1.json", "w") as f:
        #     f.write(json_data)

        print("Data saved to data.json")
        return Result(
            Data=Response(
                Cards=cards,
                Charts=charts,
                Tables=tables,
                Slicer=slicers,
                AdvancedSlicer=advancedSlicer,
                FilterValues=filters,
            ),
            Status=1,
            Message="Success",
        )
    except Exception as ex:
        message = f"Error occur at formatData: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
