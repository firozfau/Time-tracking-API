from fastapi import FastAPI,Request, HTTPException
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from routes.authRoute import auth
from routes.eventRoute import event
from routes.reportRoute import report
from routes.generalRoute import general


# Load environment variables from .env file
load_dotenv()

# Get environment variables
documents_location = os.environ.get("DOCUMENTS_LOCATION")
title = os.environ.get("TITLE")
version = os.environ.get("VERSION")
openapi_url = os.environ.get("OPEN_API_URL")
description = os.environ.get("DESCRIPTION")
info_description = os.environ.get("INFO_DESCRIPTION")
info_terms_condition = os.environ.get("INFO_TERMS_CONDITION")
info_contact_name = os.environ.get("INFO_CONTACT_NAME")
info_contact_email = os.environ.get("INFO_CONTACT_EMAIL")
allowed_ips = [ip.strip() for ip in os.environ.get("ALLOWED_IPS", "").strip('"').split(",")]


# Create FastAPI app
app = FastAPI(
    title=title,
    version=version,
    openapi_url=openapi_url,
    description=description,
    info=dict(
        description=info_description,
        terms_of_service=info_terms_condition,
        contact={
            "name": info_contact_name,
            "email": info_contact_email,
        },
    ),
)

# Include authentication routes
app.include_router(auth)
app.include_router(general)
app.include_router(event)
app.include_router(report)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, adjust as needed
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods, adjust as needed
    allow_headers=["*"],  # Allow all headers, adjust as needed
)


# Middleware to check allowed IP addresses
@app.middleware("http")
async def check_ip_address(request: Request, call_next):
    client_ip = request.client.host
    if client_ip not in allowed_ips:
        raise HTTPException(status_code=403, detail="Access Forbidden")
    response = await call_next(request)
    return response



if __name__ == "__main__":
    # Run FastAPI server
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
