import time
import json

# Function to save the token to the JSON file
def saveTokenToFile(token, expiration):
    token_data = {
        "token": token,
        "expiration": expiration,
        "timestamp": time.time(),  # Store the time when the token was saved
    }
    with open("configurations/tokens.py", "w") as file:
        json.dump(token_data, file)
