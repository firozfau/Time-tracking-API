# Password.py
from passlib.context import CryptContext
import re
from itsdangerous import URLSafeTimedSerializer
import ipaddress
from datetime import datetime, date

tKEY = URLSafeTimedSerializer("TTS-FRZ")

class Password:
    def __init__(self):
        # Use bcrypt for hashing passwords
        self.password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def getHash(self, password: str) -> str:
        return self.password_context.hash(password)

    def isMatch(self, plain_password: str, hashed_password: str) -> bool:
        return self.password_context.verify(plain_password, hashed_password)

    def containsPassword(self, text: str) -> bool:
        # Define a regular expression pattern to match common password patterns
        password_pattern = re.compile(r'\b(?:password|pass|pwd|secret)\b', flags=re.IGNORECASE)

        # Search for the pattern in the text
        if password_pattern.search(text):
            return True
        else:
            return False


    def generateToken(self, email):
        return tKEY.dumps(email, salt='email-confirm')

    def verifyToken(self, token):
        try:
            # Verify the token and get the original email
            email = tKEY.loads(token, salt='email-confirm')
            #print("hello kutta -----------",email)
            return email
        except Exception as e:
            # Token verification failed
            #print(f"Error: {e}")
            #print(f"Exception Type: {type(e).__name__}")
            return None

    def isValidEmail(self, email):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return bool(re.match(email_regex, email))
