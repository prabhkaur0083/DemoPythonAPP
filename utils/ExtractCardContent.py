import re
from datetime import datetime


# ExtractFormatted Card Content
def extractCardContent(visualContent):
    try:
        # Split content by ":" or new lines
        split_content = re.split(r":|\n", visualContent)
        # Clean up any empty or whitespace items
        split_content = [item.strip() for item in split_content if item.strip()]

        # Handle cases where the content has a key-value pair or only one item
        if len(split_content) >= 2:
            key = split_content[0]
            value = split_content[1]
        else:
            key = split_content[0]
            value = "--"

        # Create a dictionary from the key-value pair
        content_dict = {key: value}
        # Convert the dictionary items to a list
        items_list = list(content_dict.items())

        # Extract and return the content for the card
        cardContent = items_list[0]
        return cardContent
    except Exception as ex:
        message = f"Error occur at extractCardContent: {ex}"
        print(f"{datetime.now()} {message}")
        return ex
