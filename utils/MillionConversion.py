import re


# Round Off Data into Million
def millionConversion(cardContent, unit):
    # Remove all non-numeric characters except decimal points
    number_str = re.sub(r"[^\d.]", "", cardContent)

    try:
        # Convert the cleaned string to a float
        number = float(number_str)

        # Round the number to the nearest million and format
        rounded_value = round(number / 1_000_000, 1)
        formatted_content = f"{unit}{rounded_value}M"
    except ValueError:
        # Handle cases where conversion fails
        formatted_content = "--"

    return formatted_content
