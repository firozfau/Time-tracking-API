from fastapi import APIRouter, UploadFile, File, HTTPException
from libraries.event_validation import *
import os
from controller.eventController import EventController
event = APIRouter()

EventController = EventController()


@event.get("/", include_in_schema=False)
@event.post("/", include_in_schema=False)
@event.put("/", include_in_schema=False)
@event.delete("/", include_in_schema=False)
@event.options("/", include_in_schema=False)
@event.head("/", include_in_schema=False)
@event.patch("/", include_in_schema=False)
async def root_endpoint():
    data = "Welcome to TTS"
    return {"message": data}

@event.get("/api/", include_in_schema=False)
@event.post("/api/", include_in_schema=False)
@event.put("/api/", include_in_schema=False)
@event.delete("/api/", include_in_schema=False)
@event.options("/api/", include_in_schema=False)
@event.head("/api/", include_in_schema=False)
@event.patch("/api/", include_in_schema=False)
async def api_endpoint():
    data = "Welcome to TTS API"
    return {"message": data}




@event.post("/api/eventAction")
async def event_action_event(request: EventActionSkeleton):
    is_valid, errors = Validation.EventActionRequest(request)
    if not is_valid:
          return {"status": "error", "message": "Validation", "data":errors}    # Return errors along with success status
    else:
        data = await EventController.eventAction(request)
        return data

@event.post("/api/activeEventList")
async def active_event(request: ActiveEventSkeleton):
    is_valid, errors = Validation.ActiveEventRequest(request)
    if not is_valid:
          return {"status": "error", "message": "Validation", "data":errors}    # Return errors along with success status
    else:
        data = await EventController.activeEvent(request)
        return data
@event.post("/api/showEventInformation")
async def show_event_information(request: ShowEventSkeleton):
    is_valid, errors = Validation.ShowEventRequest(request)
    if not is_valid:
          return {"status": "error", "message": "Validation", "data":errors}    # Return errors along with success status
    else:
        #print(request)
        data = await EventController.showEventInformation(request)
        return data

