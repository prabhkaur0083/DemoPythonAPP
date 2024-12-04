import random
import string

def generateRandomString(length=16) -> str:
    
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))
