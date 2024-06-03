from fastapi import APIRouter, UploadFile, File, HTTPException
from libraries.auth_validation import *
import os
from controller.authController import AuthController
auth = APIRouter()

authController = AuthController()


@auth.get("/", include_in_schema=False)
@auth.post("/", include_in_schema=False)
@auth.put("/", include_in_schema=False)
@auth.delete("/", include_in_schema=False)
@auth.options("/", include_in_schema=False)
@auth.head("/", include_in_schema=False)
@auth.patch("/", include_in_schema=False)
async def root_endpoint():
    data = "Welcome to TTS"
    return {"message": data}

@auth.get("/api/", include_in_schema=False)
@auth.post("/api/", include_in_schema=False)
@auth.put("/api/", include_in_schema=False)
@auth.delete("/api/", include_in_schema=False)
@auth.options("/api/", include_in_schema=False)
@auth.head("/api/", include_in_schema=False)
@auth.patch("/api/", include_in_schema=False)
async def api_endpoint():
    data = "Welcome to TTS API"
    return {"message": data}


@auth.post("/api/rTest")
async def registration(request):
    data= await authController.rTest(request)
    return data

@auth.post("/api/registration")
async def registration(request: RegistrationSkeleton):
    is_valid, errors = Validation.registrationRequest(request)
    if not is_valid:
        return {"status": "error", "message": "Validation", "data":errors}   # Return errors along with success status
    else:
        data = await authController.registration(request)
        return data

@auth.post("/api/accountVerification")
async def account_verification(request: AccountVerificationSkeleton):
    is_valid, errors = Validation.accountVerificationRequest(request)
    if not is_valid:
        return {"status": "error", "message": "Validation", "data":errors}   # Return errors along with success status
    else:
        data = await  authController.tokenVerification(request)
        return data

@auth.post("/api/login")
async def login(request: LoginSkeleton):
    is_valid, errors = Validation.loginRequest(request)
    if not is_valid:
        return {"status": "error", "message": "Validation", "data":errors}   # Return errors along with success status
    else:

        data = await authController.login(request,2)
        return data
        #return {"status": True}´

@auth.post("/api/admin")
async def admin(request: LoginSkeleton):
    is_valid, errors = Validation.loginRequest(request)
    if not is_valid:
        return {"status": "error", "message": "Validation", "data":errors}   # Return errors along with success status
    else:

        data = await authController.login(request,1)
        return data
        #return {"status": True}´

@auth.post("/api/sendNewPassword")
async def send_new_password(request: SendNewPasswordSkeleton):
    is_valid, errors = Validation.sendNewPasswordRequest(request)
    if not is_valid:
        return {"status": "error", "message": "Validation", "data":errors}   # Return errors along with success status
    else:
        data = await authController.sendNewPassword(request)
        return data

@auth.post("/api/changePassword")
async def change_password(request: ChangePasswordSkeleton):
    is_valid, errors = Validation.changePasswordRequest(request)
    if not is_valid:
        return {"status": "error", "message": "Validation", "data":errors}   # Return errors along with success status
    else:
        data = await authController.changePassword(request)
        return data

@auth.post("/api/forgetPassword")
async def forget_password(request: ForgetPasswordSkeleton):
    is_valid, errors = Validation.forgetPasswordRequest(request)
    if not is_valid:
        return {"status": "error", "message": "Validation", "data":errors}   # Return errors along with success status
    else:
        data = await authController.forgetPassword(request)
        return data



@auth.post("/api/changeAccountType")
async def change_account_type(request: ChangeAccountTypeSkeleton):
    is_valid, errors = Validation.changeAccountTypeRequest(request)
    if not is_valid:
        return {"status": "error", "message": "Validation", "data":errors}   # Return errors along with success status
    else:
        data = await authController.changeAccountType(request)
        return data



@auth.put("/api/accountStatus")
async def change_account_status(request: AccountStatusSkeleton):
    is_valid, errors = Validation.accountStatusRequest(request)
    if not is_valid:
        return {"status": "error", "message": "Validation", "data":errors}   # Return errors along with success status
    else:
        data = await authController.changeAccountStatus(request)
        return data
@auth.post("/api/accountStatus")
async def account_status(request: ShowAccountStatusSkeleton):
    is_valid, errors = Validation.showAccountStatusRequest(request)
    if not is_valid:
        return {"status": "error", "message": "Validation", "data":errors}   # Return errors along with success status
    else:
        data = await authController.accountStatus(request)
        return data


@auth.post("/api/findUser")
async def find_user(request: FindUserSkeleton):
    is_valid, errors = Validation.FindUserRequest(request)
    if not is_valid:
        return {"status": "error", "message": "Validation", "data":errors}   # Return errors along with success status
    else:
        data = await authController.findUsers(request)
        return data
@auth.post("/api/logOut")
async def logout(request: LogOutSkeleton):
    is_valid, errors = Validation.logOutRequest(request)
    if not is_valid:
        return {"status": "error", "message": "Validation", "data":errors}   # Return errors along with success status
    else:
        data = await authController.logout(request)
        return data