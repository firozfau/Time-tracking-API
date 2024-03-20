from fastapi import APIRouter, UploadFile, File, HTTPException
from libraries.default_validation import *
import os
from controller.reportController import ReportController
report = APIRouter()

ReportController = ReportController()


@report.get("/", include_in_schema=False)
@report.post("/", include_in_schema=False)
@report.put("/", include_in_schema=False)
@report.delete("/", include_in_schema=False)
@report.options("/", include_in_schema=False)
@report.head("/", include_in_schema=False)
@report.patch("/", include_in_schema=False)
async def root_endpoint():
    data = "Welcome to TTS"
    return {"message": data}

@report.get("/api/", include_in_schema=False)
@report.post("/api/", include_in_schema=False)
@report.put("/api/", include_in_schema=False)
@report.delete("/api/", include_in_schema=False)
@report.options("/api/", include_in_schema=False)
@report.head("/api/", include_in_schema=False)
@report.patch("/api/", include_in_schema=False)
async def api_endpoint():
    data = "Welcome to TTS API"
    return {"message": data}



@report.post("/api/showReport")
async def show_report(request: ShowReportSkeleton):
    is_valid, errors = Validation.ShowReportRequest(request)
    if not is_valid:
        return {"status": "error", "message": "Validation", "data":errors}   # Return errors along with success status
    else:
        return {"success": True}

