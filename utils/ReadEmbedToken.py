import os
import json

def readTokenFromFile():
    filePath = "configurations/tokens.py"
    if os.path.exists(filePath):
        with open(filePath, "r") as file:
            token_data = json.load(file)
            return token_data
    return None


