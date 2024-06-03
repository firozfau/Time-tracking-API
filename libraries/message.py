import os
class Message:
    def __init__(self):
        pass

    def insertMessage(self, status,messages=False,data=False):
        if status=="success":
            return {
                "status": "success",
                "message": "Your insert request is successfully done.",
                "data": data
            }
        elif status=="failed":
            return {
                "status": "error",
                  "message": "Your requested information does not exist." if messages == False else None,
                "data": data
            }
        elif status == "exist":
            return {
                "status": "error",
                "message": "Your information already exist." if messages == False else None,
                "data": ""
            }
        else:
            return {
                "status": "error",
                "message": "Something is wrong. Please try again or communicate with support.",
                "redirect": False,
                "data": data
            }

    def updateMessage(self, status, messages=False, data=False):
        if status == "success":
            return {
                "status": "success",
                "message": "Your update request is successfully done.",
                "data": data
            }
        elif status == "failed":
            return {
                "status": "error",
                  "message": "Your requested information does not exist." if messages == False else None,
                "data": data
            }
        else:
            return {
                "status": "error",
                "message": "Something is wrong. Please try again or communicate with support.",
                "redirect": False,
                "data": data
            }

    def getMessage(self, status, messages=False, data=False):
        if status == "success":
            return {
                "status": "success",
                "message": "Your request is successfully done.",
                "data": data
            }
        elif status == "notExist":
            return {
                "status": "success",
                "message": "Your requested information does not exist." if messages == False else None,
                "data": data
            }

        elif status == "exist":
            return {
                "status": "success",
                  "message": "Your requested information already exist." ,
                "data": data
            }
        elif status == "failed":
            return {
                "status": "error",
                  "message": "Your requested information does not exist." if messages == False else None,
                "data": data
            }
        else:
            return {
                "status": "error",
                "message": "Something is wrong. Please try again or communicate with support.",
                "redirect": False,
                "data": data
            }


    def default(self, status, data=False):
        if status == "success":
            return {
                "status": "success",
                "message": "Successfully done.",
                "data": data
            }
        elif status == "notExist":
            return {
                "status": "success",
                "message": "Your request is valid, however, we were unable to locate any information.",
                "data": data
            }
        elif status == "sql":
            return {
                "status": "error",
                "message": "Potential SQL injection attack detected: Please provide valid data and ensure no unauthorized characters are included.",
                "data": data
            }
        else:
            return {
                "status": "error",
                "message": "Your requested information is not valid. Please provide valid and required information.",
                "redirect": False,
                "data": data
            }


    def registraion(self, status, data=False):
        if status == "success":
            return {
                "status": "success",
                "message": "Your registration is successfully done. Please check your email for further instructions and verify your account by clicking on the provided link. Thank you!",
                "data": data
            }
        elif status == "failed":
            return {
                "status": "error",
                "message": "Your registration request has failed. Please try again or contact our support team for assistance." ,
                "data": data
            }
        elif status == "email":
            return {
                "status": "error",
                  "message": "The email you provided is already associated with another account. Please use a different email address to proceed with registration.",
                "data": data
            }
        elif status == "username":
            return {
                "status": "error",
                  "message": "The selected username is currently in use. Please select an alternative username to proceed with your registration." ,
                "data": data
            }
        elif status == "password":
            return {
                "status": "error",
                "message": "The password entered does not match the retype password. Please ensure they are identical and try again.",
                "data": data
            }
        else:
            return {
                "status": "error",
                "message": "Something is wrong. Please try again or communicate with support.",
                "redirect": False,
                "data": data
            }

    def isValidInputMgs(self, status, data=False):
        if status == "success":
            return {
                "status": "success",
                "message": "The input data is correct and valid, however, our system does not contain any corresponding information.",
                "data": data
            }
        else:
            return {
                "status": "error",
                "message": "We apologize, but the input data provided does not meet the required format or specifications. Please ensure that the data is accurately formatted and meets all necessary criteria for validation.",
                "redirect": False,
                "data": data
            }

    def getEventMessage(self, status, data=False):
        if status == "success":
            return {
                "status": "success",
                "message": "Your request is successfully accepted.",
                "data": data
            }
        elif status == "exist":
            return {
                "status": "success",
                "message": "Your request is already active. No further action is required.",
                "data": data
            }
        elif status == "invalidToken":
            return {
                "status": "error",
                "message": "The user login session token you entered, that is not valid. Please check and try again.",
                "data": data
            }
        elif status == "sessionTimeout":
            return {
                "status": "error",
                "message": "Your login session has timed out. Please create a new login and resend your request.",
                "data": data
            }
        elif status == "needArrival":
            return {
                "status": "error",
                "message": "Invalid request! Please make first arrival request.",
                "data": data
            }
        elif status == "invalidRequest":
            return {
                "status": "error",
                "message":"Invalid request! Please follow the rules.",
                "data": data
            }
        else:
            return {
                "status": "error",
                "message": "We apologize, Something is wrong! Please try again!",
                "redirect": False,
                "data": data
            }