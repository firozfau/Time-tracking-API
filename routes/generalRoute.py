from fastapi import APIRouter, UploadFile, File, HTTPException
from libraries.default_validation import *
import os
from controller.generalController import GeneralController
general = APIRouter()

GeneralController = GeneralController()


@general.get("/", include_in_schema=False)
@general.post("/", include_in_schema=False)
@general.put("/", include_in_schema=False)
@general.delete("/", include_in_schema=False)
@general.options("/", include_in_schema=False)
@general.head("/", include_in_schema=False)
@general.patch("/", include_in_schema=False)
async def root_endpoint():
    data = "Welcome to TTS"
    return {"message": data}

@general.get("/api/", include_in_schema=False)
@general.post("/api/", include_in_schema=False)
@general.put("/api/", include_in_schema=False)
@general.delete("/api/", include_in_schema=False)
@general.options("/api/", include_in_schema=False)
@general.head("/api/", include_in_schema=False)
@general.patch("/api/", include_in_schema=False)
async def api_endpoint():
    data = "Welcome to TTS API"
    return {"message": data}



@general.post("/api/accountTypes")
async def account_types_general(request: CheckIPSkeleton):
    is_valid, errors = Validation. checkIPRequest(request)
    if not is_valid:
        return {"status": "error", "message": "Validation", "data":errors}    # Return errors along with success status
    else:
        data = await GeneralController.accountTypeList(request)
        return data
@general.put("/api/updateAccountAccess")
async def update_account_access_general(request: UpdateAccountTypesSkeleton):
    is_valid, errors = Validation. UpdateAccountTypesRequest(request)
    if not is_valid:
        return {"status": "error", "message": "Validation", "data":errors}    # Return errors along with success status
    else:
        data = await GeneralController.updateAccountAccess(request)
        return data

@general.post("/api/dayNameList")
async def day_name_list_general(request: CheckIPSkeleton):
    is_valid, errors = Validation. checkIPRequest(request)
    if not is_valid:
        return {"status": "error", "message": "Validation", "data":errors}    # Return errors along with success status
    else:
        data = await GeneralController.dayNameList(request)
        return data


@general.post("/api/monthNameList")
async def month_name_list_general(request: CheckIPSkeleton):
    is_valid, errors = Validation. checkIPRequest(request)
    if not is_valid:
        return {"status": "error", "message": "Validation", "data":errors}    # Return errors along with success status
    else:
        data = await GeneralController.monthNameList(request)
        return data

@general.post("/api/weekendList")
async def weekend_list_general(request: CheckIPSkeleton):
    is_valid, errors = Validation. checkIPRequest(request)
    if not is_valid:
        return {"status": "error", "message": "Validation", "data":errors}    # Return errors along with success status
    else:
        data = await GeneralController.weekendList(request)
        return data


@general.post("/api/addWeekend")
async def addWeekend_config_general(request: AddWeekendConfigSkeleton):
    is_valid, errors = Validation. AddWeekendConfigRequest(request)
    if not is_valid:
        return {"status": "error", "message": "Validation", "data":errors}    # Return errors along with success status
    else:
        data = await GeneralController.addWeekend(request)
        return data
@general.put("/api/updateWeekend")
async def updateWeekend_config_general(request: UpdateWeekendConfigSkeleton):
    is_valid, errors = Validation. UpdateWeekendConfigRequest(request)
    if not is_valid:
        return {"status": "error", "message": "Validation", "data":errors}    # Return errors along with success status
    else:
        data = await GeneralController.updateWeekend(request)
        return data

@general.post("/api/departmentNameList")
async def department_name_list_general(request: CheckIPSkeleton):
    is_valid, errors = Validation. checkIPRequest(request)
    if not is_valid:
        return {"status": "error", "message": "Validation", "data":errors}    # Return errors along with success status
    else:
        data = await GeneralController.departmentNameList(request)
        return data


@general.post("/api/designationNameList")
async def designation_name_list_general(request: CheckIPSkeleton):
    is_valid, errors = Validation. checkIPRequest(request)
    if not is_valid:
        return {"status": "error", "message": "Validation", "data":errors}    # Return errors along with success status
    else:
        data = await GeneralController.designationNameList(request)
        return data

@general.post("/api/eventNameList")
async def event_name_list_general(request: CheckIPSkeleton):
    is_valid, errors = Validation. checkIPRequest(request)
    if not is_valid:
        return {"status": "error", "message": "Validation", "data":errors}    # Return errors along with success status
    else:
        data = await GeneralController.eventNameList(request)
        return data


@general.post("/api/accessIPList")
async def access_ip_list_general(request: CheckIPSkeleton):
    is_valid, errors = Validation. checkIPRequest(request)
    if not is_valid:
        return {"status": "error", "message": "Validation", "data":errors}    # Return errors along with success status
    else:
        data = await GeneralController.accessIPList(request)
        return data

@general.post("/api/addAccessIPList")
async def add_access_ip_list_general(request: AccessIPListSkeleton):
    is_valid, errors = Validation. AccessIPListRequest(request)
    if not is_valid:
        return {"status": "error", "message": "Validation", "data":errors}    # Return errors along with success status
    else:
        data = await GeneralController.addAccessIPList(request)
        return data

@general.put("/api/updateAccessIPList")
async def update_access_ip_general(request: AccessIPUpdateSkeleton):
    is_valid, errors = Validation. AccessIPUpdateRequest(request)
    if not is_valid:
        return {"status": "error", "message": "Validation", "data":errors}    # Return errors along with success status
    else:
        data = await GeneralController.updateAccessIPList(request)
        return data

@general.post("/api/officeList")
async def office_list_general(request: CheckIPSkeleton):
    is_valid, errors = Validation. checkIPRequest(request)
    if not is_valid:
        return {"status": "error", "message": "Validation", "data":errors}    # Return errors along with success status
    else:
        data = await GeneralController.officeList(request)
        return data


@general.post("/api/addNewOfficeInformation")
async def add_new_office_general(request: OfficeConfigSkeleton):
    is_valid, errors = Validation. OfficeConfigRequest(request)
    if not is_valid:
        return {"status": "error", "message": "Validation", "data":errors}    # Return errors along with success status
    else:
        data = await GeneralController.addNewOfficeInformation(request)
        return data

@general.put("/api/updateOfficeInformation")
async def update_Office_general(request: OfficeConfigUpdateSkeleton):
    is_valid, errors = Validation. OfficeConfigUpdateRequest(request)
    if not is_valid:
        return {"status": "error", "message": "Validation", "data":errors}    # Return errors along with success status
    else:
        data = await GeneralController.updateOfficeInformation(request)
        return data




@general.post("/api/userConfigList")
async def user_config_list_general(request: UserConfigListSkeleton):
    is_valid, errors = Validation. userConfigListRequest(request)
    if not is_valid:
        return {"status": "error", "message": "Validation", "data":errors}    # Return errors along with success status
    else:
        data = await GeneralController.userConfigList(request)
        return data


@general.post("/api/addUserConfig")
async def add_user_config_general(request: UserConfigSkeleton):
    is_valid, errors = Validation. userConfigRequest(request)
    if not is_valid:
        return {"status": "error", "message": "Validation", "data":errors}    # Return errors along with success status
    else:
        data = await GeneralController.addUserConfig(request)
        return data

@general.put("/api/updateUserConfig")
async def update_user_config_general(request: UserConfigUpdateSkeleton):
    is_valid, errors = Validation. userConfigUpdateRequest(request)
    if not is_valid:
        return {"status": "error", "message": "Validation", "data":errors}    # Return errors along with success status
    else:
        data = await GeneralController.updateUserConfig(request)
        return data



@general.post("/api/holidayList")
async def holiday_config_general(request: ShowHolidayConfigListSkeleton):
    is_valid, errors = Validation. showHolidayConfigListRequest(request)
    if not is_valid:
        return {"status": "error", "message": "Validation", "data":errors}    # Return errors along with success status
    else:
        data = await GeneralController.holidayList(request)
        return data
@general.post("/api/addHolidayList")
async def add_holiday_config_general(request: HolidayConfigSkeleton):
    is_valid, errors = Validation. HolidayConfigRequest(request)
    if not is_valid:
        return {"status": "error", "message": "Validation", "data":errors}    # Return errors along with success status
    else:
        data = await GeneralController.addHolidayList(request)
        return data

@general.put("/api/updateHolidayList")
async def update_holiday_config_update_general(request: HolidayConfigUpdateSkeleton):
    is_valid, errors = Validation. holidayConfigUpdateRequest(request)
    if not is_valid:
        return {"status": "error", "message": "Validation", "data":errors}    # Return errors along with success status
    else:
        data = await GeneralController.updateHolidayList(request)
        return data

