# authController
from models.authModel import AuthModel
from libraries.message import Message
from libraries.frz import  Frz
from libraries.validation import  Validation
from libraries.password import Password
from libraries.jsonFormate import JsonFormate
from libraries.dotDict import DotDict

class AuthController:
    def __init__(self):
        self.authModel = AuthModel()
        self.mgsLib = Message()
        self.Frz = Frz()
        self.validation = Validation()
        self.PSW = Password()
        self.JSON = JsonFormate()
        self.DOT = DotDict()


    async def isSqlContentInBaseData(self, data):

        isSqlUserName = await self.validation.isSQLInjectionContent(data.username)
        isSqlFirstName = await self.validation.isSQLInjectionContent(data.first_name)
        isSqlLastName = await self.validation.isSQLInjectionContent(data.last_name)
        isSqlComments = await self.validation.isSQLInjectionContent(data.comments)
        isSqlEmail = await self.validation.isSQLInjectionContent(data.email)
        isSqlPassword = await self.validation.isSQLInjectionContent(data.password)
        if isSqlUserName:
            return True
        elif isSqlFirstName:
            return True
        elif isSqlLastName:
            return True
        elif isSqlComments:
            return True
        elif isSqlEmail:
            return True
        elif isSqlPassword:
            return True
        else:
            return False

    async def rTest(self, data):

        from libraries.mailbox import Mailbox
        Mail=Mailbox()

        email_subject = await Mail.authEmailSubject("changePass")

        mailObject = {
            'to_email': "firozfau@gmail.com",
            'subject': email_subject,
            'full_name': "firoz",
            'user_name': "SCDppos",
            'password': "sdfsdfsSss3",
            'website_link': "http://localhost:8080/admin/userList"

        }
        result = await Mail.authEmailNotification("changePass", mailObject)

    async def registration(self, data):

        if data:
            isSqlData= await  self.isSqlContentInBaseData(data)
            if isSqlData:
                return self.mgsLib.default("sql")
            else:

                isTestEmail= self.Frz.isTestEmail(data.email)

                if isTestEmail==False:
                    sqlEmail = await  self.authModel.getData(data, "byEmail")
                    if (sqlEmail.get('status') == "success"):
                        return self.mgsLib.registraion("email", data)



                sqlUser = await  self.authModel.getData(data, "byUsername")
                if(sqlUser.get('status')=="success"):
                    return self.mgsLib.registraion("username",data)
                else:
                    if len(data.password)>=2:

                        if data.password==data.confirmPassword:

                            encrypted_password = self.PSW.getHash(data.password)
                            eToken = self.PSW.generateToken(data.email)

                            required_data={
                                "encrypted_password":encrypted_password,
                                "verify_token": eToken,
                                "user_group_id":await self.Frz.defaultUserTypeGroupID(),
                                "account_type_id":await self.Frz.defaultUserTypeID(),
                            }

                            #print(required_data)
                            sqlData = await  self.authModel.insertData(data,required_data, "userRegistration")

                            if sqlData['status']=="success":

                                registrationData={
                                    "user_id":sqlData['data'],
                                    "first_name": data.first_name,
                                    "last_name": data.last_name,
                                    "username": data.username,
                                    "email": data.email,
                                    "mobile_number": data.mobile_number,
                                    "verify_token": eToken,
                                    "encrypted_password": encrypted_password,
                                }

                                emailData={
                                   "user_id":registrationData['user_id'],
                                    "password": data.password,
                                }


                                await self.autEmailNotification("userRegi", data, emailData)  # send information to the user email

                                return self.mgsLib.registraion("success", registrationData)


                            else:
                                return self.mgsLib.registraion("failed", data)

                        else:
                            return self.mgsLib.registraion("password", data)

                    else:
                        return self.mgsLib.registraion("password", data)



        else:
            return self.mgsLib.default(False)

    async def login(self, data,account_type):

        # 1->admin
        # 2-> others


        if data:

            checkIP = await self.checkWhiteIP(data.user_ip)

            if checkIP['status']:

                isSqlInjection = await self.validation.isSQLInjectionContent(data.username)

                if isSqlInjection:
                    return self.mgsLib.default("sql")
                else:
                    sqlData = await  self.authModel.getData(data, "byUsername")

                    if (sqlData.get('status') == "success"):

                        dbData = sqlData.get('data')
                        encryptedPassword = dbData[0].get('password')
                        account_type_id = dbData[0].get('account_type_id')
                        user_group_id = dbData[0].get('user_group_id')

                        checkPassword = await self.verifyPassword(data.password, encryptedPassword)

                        if checkPassword['status'] == "success":
                            accountStatus = await self.checkAccountStatus(dbData[0].get('status'))


                            if accountStatus['status'] == "success":
                                accountTypeCheck = await self.accountTypeCheck(account_type,user_group_id)

                                #print(account_type,"----",accountTypeCheck)
                                #print(dbData[0], "------_____________________________--->",accountTypeCheck)

                                if accountTypeCheck['status'] == "success":


                                    loginSessionData = await self.getLoginSession(dbData[0],data)

                                    if loginSessionData:
                                        return self.mgsLib.getMessage(sqlData.get('status'), False, loginSessionData)
                                    else:
                                        return self.mgsLib.getMessage("error", False, False)
                                else:
                                    return accountTypeCheck
                            else:
                                return accountStatus
                        else:
                            return checkPassword

                    else:
                        return {
                            "status": "error",
                            "message": "Your username does not exist. Please enter your correct username.",
                            "data": data
                        }

            else:

                return {
                    "status": "error",
                    "message": checkIP['message'],
                    "data":data
                }
        else:
            return self.mgsLib.default(False)

    async def logout(self,data):
        if data:

            checkIP = await self.checkWhiteIP(data.user_ip)

            if checkIP['status']:

                loginData= await self.authModel.loginDataByToken(data.sessionToken,data.user_id)

                if loginData:

                    objectData=self.JSON.getDecodedData(loginData)['data']

                    utcData = await self.authModel.getUserTTSConfigInformation(objectData['user_id'])
                    dbData = self.JSON.getDecodedData(utcData).get('data')
                    currentDateObject = await self.Frz.getDateTimeByUTC(int(dbData['time_zone']))
                    user_utc_logout_time = currentDateObject['date_time']


                    longSessionStatus= await self.loginSessionDestroyed(objectData['user_id'], user_utc_logout_time)
                    if longSessionStatus:
                        return {
                            "status": "success",
                            "message": "Your request has been successfully processed. Your login session has been terminated.",
                            "data": data
                        }
                    else:
                        return {
                            "status": "error",
                             "message": "Something is wrong. Please try again or communicate with support.",
                            "data": data
                        }

                else:
                    return {
                        "status": "error",
                        "message": "The provided token is currently inactive. Please provide a valid token.",
                        "data": data
                    }

            else:

                return {
                    "status": "error",
                    "message": checkIP['message'],
                    "data":data
                }
        else:
            return self.mgsLib.default(False)
    async def loginSessionDestroyed(self,user_id,user_utc_logout_time,logout_by=1,comments=""):
        sessionDestroyed= await self.authModel.userLoginUpdate(user_id,user_utc_logout_time, logout_by, comments)

        if sessionDestroyed=="success":
            return  True
        else:
            return  False
    async def isCurrentLoginStatus(self, user_id,isLogoutAction=False):
        isLoginSessionActive =await self.authModel.getLoginHistoryByID(user_id, "1")

        if isLoginSessionActive:

            loginSessionObject=  self.JSON.getDecodedData(isLoginSessionActive)['data']
            utcData = await self.authModel.getUserTTSConfigInformation(user_id)

            dbData = self.JSON.getDecodedData(utcData).get('data')
            currentDateObject= await self.Frz.getDateTimeByUTC(int(dbData['time_zone']))
            currentDateTimeString = currentDateObject['date_time']
            dBDateTimeString = loginSessionObject['user_utc_login_time']


            isTimeOver = await self.Frz.isOverDateTime(currentDateTimeString,dBDateTimeString ,dbData['work_end_time'])

            if isTimeOver:
                if isLogoutAction:
                    logoutResult = await  self.loginSessionDestroyed(user_id,currentDateObject['date_time'], 2,"time is over then system auto logout")
                    if logoutResult:
                        return {
                            "status": False,
                            "utcStatus": False,
                            "data": isLoginSessionActive
                        }
                    else:
                        return {
                            "status": True,  # still login session running
                            "utcStatus": False,  ## as per utc default time is over, should be logout by system
                            "data": isLoginSessionActive
                        }
                else:
                    return {
                        "status": True,  # still login session running
                        "utcStatus": False,  ## as per utc default time is over, should be logout by system
                        "data": isLoginSessionActive
                    }

            else:
                return {
                    "status": True,  # still login session running
                    "utcStatus": True,  ## time is available
                    "data": isLoginSessionActive
                }

        else:
            return {
                "status": False,
                "utcStatus": False,
                "data": False
            }


    async def getLoginSession(self,data,requestData):

        user_id = data.get("id")

        utcData = await self.authModel.getUserTTSConfigInformation(user_id)
        utcDbData = self.JSON.getDecodedData(utcData).get('data')
        user_utc_current_date = await self.Frz.getDateTimeByUTC(int(utcDbData['time_zone']), True)


        userData = {
            "office_id": data.get("office_id"),
            "user_group_id": data.get("user_group_id"),
            "account_type_id": data.get("account_type_id"),
            "user_id": data.get("id"),
            "account_status": data.get("status"),
            "username": data.get("username"),
            "first_name": data.get("first_name"),
            "last_name": data.get("last_name"),
            "email": data.get("email"),
            "department_id": data.get("department_id"),
            "designation_id": data.get("designation_id"),
            "gender": data.get("gender"),
            "registration_date": data.get("created_at"),
            "user_ip": data.get("user_ip"),
            "user_photo": data.get("user_photo"),
            "login_session_id": "",
            "login_session_Token": "",
            "login_time": "",
            "login_status": "",
            "login_ip":"",
            "user_utc_time_zone":utcDbData['time_zone'],
            "user_utc_login_date_time": user_utc_current_date

        }


        #print(userData)

        currentStatus= await self.isCurrentLoginStatus(user_id,True)



        if currentStatus['status']==True and currentStatus['utcStatus']==False:
            return False

        elif currentStatus['status'] == True and currentStatus['utcStatus'] == True:
            objectData=self.JSON.getDecodedData(currentStatus['data'])['data']

            userData['login_session_id'] = objectData['id']
            userData['login_session_Token'] = objectData['sessionToken']
            userData['login_time'] = objectData['user_utc_login_time']
            userData['login_status'] = True
            userData['login_ip'] = requestData.user_ip


            return userData
        else:

            user_ip = requestData.user_ip
            currentTimeStamp =str(await self.Frz.getCurrentTimeStamp())
            sessionToken = self.PSW.getHash(currentTimeStamp)

            utcData = await self.authModel.getUserTTSConfigInformation(user_id)


            dbData = self.JSON.getDecodedData(utcData).get('data')

            currentDateObject = await self.Frz.getDateTimeByUTC(int(dbData['time_zone']))


            loginSessionObject={
                "user_id":user_id,
                "sessionToken": sessionToken,
                "user_ip": user_ip,
                "user_utc_login_time":currentDateObject['date_time'],
                "comments": ""
            }

            loginSession =self.DOT.convert_to_dotdict(loginSessionObject)

            sqlData = await  self.authModel.insertData(loginSession, False, "userLoginInsert")
            if sqlData['status']=="success":
                userData['login_session_id']=sqlData['data']
                userData['login_session_Token'] =sessionToken
                userData['login_time'] = currentDateObject['date_time']
                userData['login_status'] =True
                userData['login_ip'] = user_ip

                return userData
            else:
                return False


    async def checkWhiteIP(self, requestedIP):
        sqlUser = await  self.authModel.matchWhiteIP(requestedIP)

        if sqlUser:
            dSqlData= self.JSON.getDecodedData(sqlUser)

            if dSqlData['data']['status']==1:
                return {
                    "status": True,
                    "message": "The requested IP is allowed."
                }
            else:
                return {
                    "status": False,
                    "message": "The requested IP is blocked. Please contact our support team for assistance."
                }

        else:
            return {
                "status":False,
                "message":"The requested IP whitelist could not be found"
            }


    async def tokenVerification(self,data):
        verify_token=data.verify_token
        user_ip = data.user_ip

        if user_ip and verify_token:
            checkIP=  await self.checkWhiteIP(user_ip)
            #print(checkIP)

            if checkIP['status']:

                email_address =  self.PSW.verifyToken(verify_token)
                if email_address:
                    isValidEmail = self.PSW.isValidEmail(email_address)
                    if isValidEmail:
                        sqlUser = await  self.authModel.byUserOpenKey(email_address,"email")
                        if sqlUser:
                            dSqlData = self.JSON.getDecodedData(sqlUser)
                            user_id = dSqlData['data']['id']

                            if dSqlData['data']['email_verify_status']==0:

                                email_verify_status = await self.authModel.updateSingleValueOfUser(user_id,"email_verify_status",1)

                                if email_verify_status == "success":
                                    accountStatus = await self.authModel.updateSingleValueOfUser(user_id, "status", 1)
                                    if accountStatus == "success":

                                        DBdata = {
                                            "first_name": dSqlData['data']['first_name'],
                                            "last_name": dSqlData['data']['last_name'],
                                            "email": dSqlData['data']['email'],
                                            "username": dSqlData['data']['username'],
                                            "verify_token":verify_token
                                        }

                                        return {
                                            "status": "success",
                                            "message": "Your account has been successfully verified and is now active.",
                                            "data": DBdata
                                        }


                                    else:
                                        return {
                                            "status": "error",
                                            "message": "Something is wrong. Your email has been verified, but your account is not yet active. Please contact support for assistance.",
                                            "data": ""
                                        }

                                else:
                                    return {
                                        "status": "error",
                                        "message": "Something is wrong. Please try again or communicate with support.",
                                        "data": ""
                                    }

                            else:
                                return {
                                    "status": "error",
                                    "message": "Your account has already been verified.",
                                    "data": ""
                                }

                        else:
                            return {
                                "status": "error",
                                "message": "The user verification token is invalid. Please provide a valid one, which will be found in the email.",
                                "data": ""
                            }

                    else:
                        return {
                            "status": "error",
                            "message": "The user verification token is invalid. Please provide a valid one, which will be found in the email.",
                            "data": ""
                        }
                else:
                    return {
                        "status": "error",
                        "message": "The user verification token is invalid. Please provide a valid one, which will be found in the email.",
                        "data": ""
                    }
            else:
                return {
                    "status": "error",
                    "message": checkIP['message'],
                    "data": ""
                }
        else:
            return {
                "status": "error",
                "message": "Both the IP address and the token are mandatory.",
                "data": ""
            }

    async  def verifyPassword(self,rawPassword,encryptedPassword):

        if len(encryptedPassword)>20:
            isMatchPassword = self.PSW.isMatch(rawPassword, encryptedPassword)

            if isMatchPassword:
                return {
                    "status": "success",
                    "message": "Your password matches the expected one." ,
                    "data": ""
                }
            else:
                return {
                    "status": "error",
                    "message": "Your password does not match the expected one.",
                    "data": ""
                }
        else:
            return {
                "status": "error",
                "message": "Something went wrong with your authentication. Please contact the support team to reset your password.",
                "data": ""
            }

    async  def checkAccountStatus(self,accountStatus):

        if accountStatus==0 or  accountStatus=="":
            return {
                "status": "error",
                "message": "Your account is still not verified. Please verify your account first" ,
                "data": ""
            }
        elif accountStatus ==2:
            return {
                "status": "error",
                "message": "Your account is currently inactive. Please contact support for further assistance.",
                "data": ""
            }
        elif accountStatus == 3:
            return {
                "status": "error",
                "message": "Your account is currently Blocked. Please contact support for further assistance.",
                "data": ""
            }
        elif accountStatus == 4:
            return {
                "status": "error",
                "message": "We couldn't find your account in our system. Please contact support for assistance.",
                "data": ""
            }
        elif accountStatus == 1:
            return {
                "status": "success",
                "message": "Your account is active",
                "data": ""
            }
        else:
            return {
                "status": "error",
                "message": "Something is wrong. Please try again or communicate with support.",
                "data": ""
            }

    async def accountTypeCheck(self, accountTypeID, user_group_id):

        if accountTypeID == 0 or accountTypeID == "":
            return {
                "status": "error",
                "message": "Your request is not acceptable. Please communicate with the support team.",
                "data": ""
            }
        else:
            if accountTypeID == 1 and user_group_id in range(1, 5):
                return {
                    "status": "success",
                    "message": "Request is okay",
                    "data": ""
                }
            elif accountTypeID == 2 and user_group_id in range(5, 11):
                return {
                    "status": "success",
                    "message": "Request is okay",
                    "data": ""
                }
            else:
                return {
                    "status": "error",
                    "message": "Your request is not acceptable. Please communicate with the support team.",
                    "data": ""
                }

    # auth second part-----------------------------------------------------------------------------------------------
    """
    async def skelton(self,data):
           if data:
    
               checkIP = await self.checkWhiteIP(data.user_ip)
    
               if checkIP['status']:
                    
                    return 1
    
               else:
    
                   return {
                       "status": "error",
                       "message": checkIP['message'],
                       "data":data
                   }
           else:
               return self.mgsLib.default(False)
    """


    async def sendNewPassword(self, data):
        if data:

            checkIP = await self.checkWhiteIP(data.user_ip)

            if checkIP['status']:

                user_id= data.user_id
                raw_password=await self.Frz.geRandomPassword(5)
                encrypted_password = self.PSW.getHash(raw_password)
                #print(raw_password)

                updatePassword= await self.authModel.updateSingleValueOfUser(user_id,"password",encrypted_password)
                if updatePassword=="success":


                    emailData = {
                        "user_id": user_id,
                        "password": raw_password,
                    }
                    await self.autEmailNotification("sendPass", data,emailData)  # send information to the user email

                    return {
                        "status": "success",
                        "message": "Your password has been successfully updated. Please use the new password for future logins.",
                        "data": {
                            "user_id":user_id,
                            "raw_password": raw_password,
                        }
                    }
                else:
                    return self.mgsLib.default(False)
            else:

                return {
                    "status": "error",
                    "message": checkIP['message'],
                    "data": data
                }
        else:
            return self.mgsLib.default(False)


    async def changePassword(self, data):
        if data:

            checkIP = await self.checkWhiteIP(data.user_ip)

            if checkIP['status']:

                #F8daS

                isSqlNewPassword = await self.validation.isSQLInjectionContent(data.new_password)
                isSqlCurrentPassword = await self.validation.isSQLInjectionContent(data.current_password)

                if isSqlNewPassword or  isSqlCurrentPassword:
                    return self.mgsLib.default("sql")
                else:

                    userData = await  self.authModel.getData(data, "byUserId")

                    if userData:

                        if userData['status']=="success":


                            encryptedPassword = userData['data'][0]['password']
                            checkPassword = await self.verifyPassword(data.current_password, encryptedPassword)
                            if checkPassword['status']=="success":

                                user_id = userData['data'][0]['id']
                                raw_password = data.new_password
                                encrypted_password = self.PSW.getHash(raw_password)

                                updatePassword = await self.authModel.updateSingleValueOfUser(user_id, "password",
                                                                                              encrypted_password)
                                if updatePassword == "success":

                                    emailData = {
                                        "user_id": user_id,
                                        "password": raw_password,
                                    }

                                    await self.autEmailNotification("changePass",data,emailData)  # send information to the user email

                                    return {
                                        "status": "success",
                                        "Validation": False,
                                        "message": "Your password has been successfully updated. Please use the new password for future logins.",
                                        "data": {
                                            "user_id": user_id,
                                            "raw_password": raw_password,
                                        }
                                    }
                                else:
                                    return {
                                        "status": "error",
                                        "Validation": False,
                                        "message": "Your request Failed !",
                                        "data": data
                                    }


                            else:
                                return {
                                    "status": "error",
                                    "Validation":"current_password",
                                    "message": "The current password does not match.",
                                    "data": data
                                }
                        else:
                            return {
                                "status": "error",
                                "Validation": False,
                                "message": "Something is wrong! please try again.",
                                "data": data
                            }

                    else:
                        return {
                            "status": "error",
                            "Validation": False,
                            "message": "User information was not found in our system.",
                            "data": data
                        }

            else:

                return {
                    "status": "error",
                    "Validation": False,
                    "message": checkIP['message'],
                    "data": data
                }
        else:
            return self.mgsLib.default(False)


    async def forgetPassword(self, data):
        if data:

            checkIP = await self.checkWhiteIP(data.user_ip)

            if checkIP['status']:

                #F8daS
                isSqlEmail = await self.validation.isSQLInjectionContent(data.email)

                if isSqlEmail:
                    return self.mgsLib.default("sql")
                else:

                    userData = await  self.authModel.getData(data, "byEmail")


                    if userData:

                        if userData['status']=="success":
                            user_id = userData['data'][0]['id']

                            raw_password = await self.Frz.geRandomPassword(5)
                            encrypted_password = self.PSW.getHash(raw_password)

                            updatePassword = await self.authModel.updateSingleValueOfUser(user_id, "password",
                                                                                          encrypted_password)
                            if updatePassword == "success":

                                emailData = {
                                    "user_id": user_id,
                                    "password": raw_password,
                                }

                                await self.autEmailNotification("forgetPass",data,emailData) # send information to the user email
                                return {
                                    "status": "success",
                                    "message": "Your password has been successfully updated. Please use the new password for future logins.",
                                    "data": {
                                        "user_id": user_id,
                                        "raw_password": raw_password,
                                    }
                                }
                            else:
                                return self.mgsLib.default(False)

                        else:
                            return {
                                "status": "error",
                                "message": "Your email was not found in our system. Please enter your registered email address.",
                                "data": data
                            }

                    else:
                        return {
                            "status": "error",
                            "message": "Your email was not found in our system. Please enter your registered email address.",
                            "data": data
                        }

            else:

                return {
                    "status": "error",
                    "message": checkIP['message'],
                    "data": data
                }
        else:
            return self.mgsLib.default(False)

    async def changeAccountType(self, data):
        if data:

            checkIP = await self.checkWhiteIP(data.user_ip)

            if checkIP['status']:

                user_id=data.user_id
                user_ip=data.user_ip
                account_type_id=data.account_type_id

                isUserID = await self.Frz.convertIntegerData(user_id)
                isUserAccountType = await self.Frz.convertIntegerData(account_type_id)
                if isUserAccountType==1:
                    return {
                        "status": "error",
                        "message": "You are not allowed to change to the super admin from any other account.",
                        "data": data
                    }

                else:

                    updateAccountType = await self.authModel.updateSingleValueOfUser(user_id, "account_type_id",account_type_id)

                    if updateAccountType=="success":
                        return {
                            "status": "success",
                            "message":"Account type successfully changed as per your request.",
                            "data": data
                        }
                    else:
                        return {
                            "status": "error",
                            "message": "Something is wrong! Please try again.",
                            "data": data
                        }

            else:

                return {
                    "status": "error",
                    "message": checkIP['message'],
                    "data": data
                }
        else:
            return self.mgsLib.default(False)

    async def changeAccountStatus(self, data):
        if data:

            checkIP = await self.checkWhiteIP(data.user_ip)

            if checkIP['status']:

                user_id=data.user_id
                user_ip=data.user_ip
                status = data.status
                comments = data.comments

                updateAccountStatus = await self.authModel.updateSingleValueOfUser(user_id, "status",status)

                if updateAccountStatus == "success":
                    if len(comments)>0:
                        updateAccountComments = await self.authModel.updateSingleValueOfUser(user_id, "comments", comments)

                    return {
                        "status": "success",
                        "message": "Account status successfully changed as per your request.",
                        "data": data
                    }
                else:
                    return {
                        "status": "error",
                        "message": "Something is wrong! Please try again.",
                        "data": data
                    }


            else:

                return {
                    "status": "error",
                    "message": checkIP['message'],
                    "data": data
                }
        else:
            return self.mgsLib.default(False)

    async def accountStatus(self, data):
        if data:

            checkIP = await self.checkWhiteIP(data.user_ip)

            if checkIP['status']:


                accountData=await  self.authModel.byUserOpenKey(data.user_id,"id")
                if accountData:
                    currentStatus = await self.isCurrentLoginStatus(data.user_id, False)
                    accountObjectData=self.JSON.getDecodedData(accountData)['data']

                    return {
                        "status": "success",
                        "message": "Successfully found your account information",
                        "data": {
                            "loginStatus":currentStatus['status'],
                            "loginUTCStatus": currentStatus['utcStatus'],
                            "account_status": await self.Frz.accountStatus(accountObjectData['status'])
                        }
                    }
                else:
                    return self.mgsLib.default(False)
            else:

                return {
                    "status": "error",
                    "message": checkIP['message'],
                    "data": data
                }
        else:
            return self.mgsLib.default(False)

    async def findUsers(self, data):
        if data:

            checkIP = await self.checkWhiteIP(data.user_ip)

            if checkIP['status']:

                isKey_data = await self.validation.isSQLInjectionContent(data.key_data)
                if isKey_data:
                    return self.mgsLib.default("sql")
                else:
                    searchData=await  self.authModel.findUsers(data.key_data)
                    if searchData:

                        userRetrievedData={
                                "key_word":data.key_data,
                                "user_data":searchData
                        }
                        return {
                            "status": "success",
                            "message": "Your requested data has been successfully retrieved.",
                            "data": userRetrievedData
                        }

                    else:
                        return {
                            "status": "success",
                            "message": "No data Found!",
                            "data": data
                        }
            else:

                return {
                    "status": "error",
                    "message": checkIP['message'],
                    "data": data
                }
        else:
            return self.mgsLib.default(False)

    async def autEmailNotification(self,actionType, data,userData):

        from libraries.mailbox import Mailbox
        Mail = Mailbox()


        user_id= userData['user_id']

        accountData = await  self.authModel.byUserOpenKey(user_id, "id")
        if accountData:
            accountObjectData = self.JSON.getDecodedData(accountData)['data']

            full_name = accountObjectData['first_name'] + " " + accountObjectData['last_name']
            website_link=await self.Frz.getWebSiteLink("web")


            if actionType=="userRegi":

                email_subject = await Mail.authEmailSubject("userRegi")

                mailObject = {
                    'to_email': accountObjectData['email'],
                    'subject': email_subject,
                    'full_name': full_name,
                    'user_name': accountObjectData['username'],
                    'password': userData['password'],
                    'website_link':website_link

                }
                result = await Mail.authEmailNotification("userRegi", mailObject)

            elif actionType == "changePass" or actionType == "forgetPass" or actionType == "sendPass":
                email_subject = await Mail.authEmailSubject("changePass")

                mailObject = {
                    'to_email': accountObjectData['email'],
                    'subject': email_subject,
                    'full_name': full_name,
                    'user_name': accountObjectData['username'],
                    'password': userData['password'],
                    'website_link': website_link

                }

                result = await Mail.authEmailNotification("changePass", mailObject)




