from core.models.report.ChartsModel import Series
from typing import List
from core.models.report.ResultModel import Result
import re
from datetime import datetime


def chartFormatting(visualData: dict):
    try:
        unit = ""
        chartcontent = visualData["VisualData"]["data"]
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
                    # Determine which value (x or y) contains a percentage or numeric data
                    if "%" in y_value:
                        numeric_value = float(re.sub(r"[^\d.-]", "", y_value))   # Handle percentage as decimal
                        x_axis.append(x_value)
                    elif "%" in x_value:
                        numeric_value = float(re.sub(r"[^\d.-]", "", x_value)) 
                        x_axis.append(y_value)
                    else:
                        # Default numeric parsing
                        try:
                            numeric_value = float(re.sub(r"[^\d.-]", "", y_value))
                            x_axis.append(x_value)
                        except:
                            numeric_value = float(re.sub(r"[^\d.-]", "", x_value))
                            x_axis.append(y_value)

                    y_axis.append(numeric_value)
                except ValueError:
                    # If parsing fails, skip this line
                    continue
                # try:
                #     unit = y_value[0][0]
                #     if "%" in y_value:
                #         # Attempt to convert y_value to a float, removing any non-numeric characters
                #         numeric_value = float(re.sub(r"[^\d.-]", "", y_value))
                #         x_axis.append(x_value)  # Append the x_value (e.g., month)
                #     else:
                #         numeric_value = float(re.sub(r"[^\d.-]", "", x_value))
                #         x_axis.append(y_value)  # Append the x_value (e.g., month)
                #     y_axis.append(numeric_value)  # Append the numeric y_value
                # except:
                    # print("No chart")
                    # try:
                    #     unit = x_value[0][0]
                    #     if "%" in x_value:
                    #         numeric_value = float(re.sub(r"[^\d.-]", "", x_value))
                    #         x_axis.append(y_value)  # Append the x_value (e.g., month)
                    #     else:
                    #         numeric_value = float(re.sub(r"[^\d.-]", "", y_value))
                    #         x_axis.append(x_value)  # Append the x_value (e.g., month)

                    #     y_axis.append(numeric_value)

                    # # # If both fail, skip this line or handle it differently as needed
                    # except:

                    #     continue

            series.append(Series(Xaxis=x_axis, Yaxis=y_axis))
        if unit.isnumeric():
            unit = ""

        responseData = {"unit": unit, "seriesData": series, "headerTitle": headers}
        return Result(Data=responseData,Status=1,Message="Data Formatted Successfully")
    
    except Exception as ex:
        message = f"Error occur at chartFormatting: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
