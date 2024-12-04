from core.models.report.ResultModel import Result
from datetime import datetime


# Function to clean a cell, extracting the date from a timestamp
def clean_cell(cell):
    # Check if the cell is a timestamp (format: YYYY-MM-DD HH:MM:SS or similar)
    if " " in cell and len(cell.split(" ")[0].split("-")) == 3:
        return cell.split(" ")[0]  # Extract only the date part
    return cell.replace("\r", "").replace('"', "")  # Clean other characters


def processTable(visual) -> Result:
    try:
        # Initialize dataUnit
        data_unit = ""

        # Extract table content and split it into lines
        table_content = visual["VisualData"]["data"]
        lines = table_content.split("\n")

        # Extract columns from the first line
        columns = lines[0].split(",")

        # Process rows, splitting each line by commas and removing empty lines
        rows = [line.split(",") for line in lines[1:] if line]

        # Clean each cell in the rows

        # Clean each cell in the rows
        cleaned_rows = [[clean_cell(cell) for cell in row] for row in rows]

        return Result(
            Data={
                "Type": visual["Type"],
                "Unit": data_unit,
                "Columns": columns,
                "Rows": cleaned_rows,
            },
            Status=1,
            Message="Data Formatted Successfully",
        )
    except Exception as ex:
        message = f"Error occur at extractVisualData: {ex}"
        print(f"{datetime.datetime.now()} {message}")
        return Result(Status=0, Message=message)
