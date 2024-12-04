import re


# Round Off Data into Thousand
def thousandsConversion(cardContent, unit):
    # Remove all non-numeric characters except decimal points
    number_str = re.sub(r"[^\d.]", "", cardContent)

    try:
        # Convert the cleaned string to a float
        number = float(number_str)

        # Round the number to the nearest thousand and format
        converted_value = round(number / 1_000, 2)
        formatted_content = f"{unit}{converted_value}K"
    except ValueError:
        # Handle cases where conversion fails
        formatted_content = "--"

    return formatted_content
