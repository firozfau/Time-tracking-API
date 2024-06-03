from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

app = FastAPI()
security = HTTPBearer()

# Your static token
static_token ="KnaKmacGaiverAleoGenoFire"

def verifyKey(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Custom dependency function to verify the token.
    """
    provided_token = credentials.credentials
    if provided_token == static_token:
        # Token is valid
        return True
    else:
        # Token is not valid, raise HTTPException
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
