import bcrypt


def hash_password(password : str) -> str:

    salt  =  bcrypt.gensalt()

    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

    # Convert bytes to string for database storage
    return hashed.decode('utf-8') 

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Compare a plain password with its hashed version.
    Returns True if they match, otherwise False.
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

