import bcrypt


#Hashing the password 
def passwordHashing(password : str):

    bytes = password.encode("utf-8")

    salt = bcrypt.gensalt()

    hash = bcrypt.hashpw(bytes, salt)

    return hash.decode("utf-8")


# Verifying the password with the stored hash
def verifyPassword(storedHash: str, inputPassword: str) -> bool:
    try:
        return bcrypt.checkpw(inputPassword.encode("utf-8"), storedHash.encode("utf-8"))
    except ValueError:
        
        return False
