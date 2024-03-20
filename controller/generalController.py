# authController
from models.authModel import AuthModel
from models.generalModel import GeneralModel
from libraries.message import Message
from libraries.frz import  Frz
from libraries.validation import  Validation
from libraries.password import Password
from libraries.jsonFormate import JsonFormate
from libraries.dotDict import DotDict
class GeneralController:
    def __init__(self):
        self.authModel = AuthModel()
        self.generalModel = GeneralModel()

        self.authModel = AuthModel()
        self.mgsLib = Message()
        self.Frz = Frz()
        self.validation = Validation()
        self.PSW = Password()
        self.JSON = JsonFormate()
        self.DOT = DotDict()


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
    async def accountTypeList(self, data):
        if data:

            checkIP = await self.checkWhiteIP(data.user_ip)

            if checkIP['status']:

               account_list=await self.Frz.accountTypeList()
               return {
                   "status": "success",
                   "message": "The account type list has been successfully retrieved",
                   "data": account_list
               }

            else:

                return {
                    "status": "error",
                    "message": checkIP['message'],
                    "data": data
                }
        else:
            return self.mgsLib.default(False)


    async def updateAccountAccess(self, data):
        if data:

            checkIP = await self.checkWhiteIP(data.user_ip)

            if checkIP['status']:

               account_type_id=data.account_type_id
               access_list=self.JSON.getObjectToJson(data.access)
               user_ip = data.user_ip
               user_id = data.user_id
               comments = data.comments

               stringAccessList=await self.Frz.getStringFromObject(data.access)
               isAccess_list = await self.validation.isSQLInjectionContent(stringAccessList)
               isComments = await self.validation.isSQLInjectionContent(comments)

               if isAccess_list or isComments:
                   return self.mgsLib.default("sql")
               else:
                   if account_type_id==1:

                       return {
                           "status": "error",
                           "message": "You are not allowed to update super Admin access",
                           "data": data
                       }
                   else:
                       updateStatus = await self.generalModel.updateAccountAccess(account_type_id, access_list, 1, comments, user_id, user_ip)

                       if updateStatus == "success":
                           return {
                               "status": "success",
                               "message": "Your request has been successfully completed.",
                               "data": data
                           }
                       else:
                           return {
                               "status": "error",
                               "message": "Unfortunately, we are unable to process your request at this time. Please contact our support team for assistance.",
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


    async def dayNameList(self, data):
        if data:

            checkIP = await self.checkWhiteIP(data.user_ip)

            if checkIP['status']:

               dayNameList= await self.generalModel.getData(data,"dayNameList")

               return {
                   "status": "success",
                   "message": "The day name list has been successfully retrieved",
                   "data": dayNameList
               }

            else:

                return {
                    "status": "error",
                    "message": checkIP['message'],
                    "data": data
                }
        else:
            return self.mgsLib.default(False)

    async def monthNameList(self, data):
        if data:

            checkIP = await self.checkWhiteIP(data.user_ip)

            if checkIP['status']:

               dayNameList= await self.generalModel.getData(data,"monthNameList")

               return {
                   "status": "success",
                   "message": "The month name list has been successfully retrieved",
                   "data": dayNameList
               }

            else:

                return {
                    "status": "error",
                    "message": checkIP['message'],
                    "data": data
                }
        else:
            return self.mgsLib.default(False)


    async def weekendList(self, data):
        if data:

            checkIP = await self.checkWhiteIP(data.user_ip)

            if checkIP['status']:

               dayNameList= await self.generalModel.getData(data,"weekendList")

               return {
                   "status": "success",
                   "message": "The weekend list has been successfully retrieved",
                   "data": dayNameList
               }

            else:

                return {
                    "status": "error",
                    "message": checkIP['message'],
                    "data": data
                }
        else:
            return self.mgsLib.default(False)


    async def addWeekend(self, data):
        if data:

            checkIP = await self.checkWhiteIP(data.user_ip)

            if checkIP['status']:

               weekend_name=data.weekend_name
               comments = data.comments
               user_id = data.user_id
               user_ip = data.user_ip
               day_name_list_id=self.JSON.getObjectToJson(data.day_name_list_id)


               stringDayNameList=await self.Frz.getNumberStringFromObject(data.day_name_list_id)
               isDayName_list = await self.validation.isSQLInjectionContent(stringDayNameList)
               isWeekend = await self.validation.isSQLInjectionContent(weekend_name)

               if isDayName_list or isWeekend:
                   return self.mgsLib.default("sql")
               else:
                   keyWord={
                       "weekend_name":weekend_name
                   }
                   searchObject= self.DOT.convert_to_dotdict(keyWord)
                   weekEndObj= await  self.generalModel.getData(searchObject,"weekendListByName")

                   if weekEndObj['status']=="success":

                       return {
                           "status": "error",
                           "message": "This weekend name already exists. Please choose a different one.",
                           "data": data
                       }
                   else:
                       objectInsert={
                                     'weekend_name': weekend_name,
                                     'comments': comments,
                                     'created_id': user_id,
                                     'user_ip': user_ip,
                                     'day_name_list_id': day_name_list_id,
                                 }
                       insertDistObject =self.DOT.convert_to_dotdict(objectInsert)

                       addWeekendData = await self.generalModel.insertData(insertDistObject,"","addWeekend")

                       if addWeekendData['status']== "success":
                           return {
                               "status": "success",
                               "message": "Your request has been successfully completed.",
                               "data": addWeekendData
                           }
                       else:
                           return {
                               "status": "error",
                               "message": "Unfortunately, we are unable to process your request at this time. Please contact our support team for assistance.",
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

    async def updateWeekend(self, data):
        if data:

            checkIP = await self.checkWhiteIP(data.user_ip)

            if checkIP['status']:

               weekend_name=data.weekend_name
               comments = data.comments
               user_id = data.user_id
               user_ip = data.user_ip
               weekend_id = data.weekend_id
               day_name_list_id=self.JSON.getObjectToJson(data.day_name_list_id)


               stringDayNameList=await self.Frz.getNumberStringFromObject(data.day_name_list_id)
               isDayName_list = await self.validation.isSQLInjectionContent(stringDayNameList)
               isWeekend = await self.validation.isSQLInjectionContent(weekend_name)

               if isDayName_list or isWeekend:
                   return self.mgsLib.default("sql")
               else:
                   weekEndIDObj={
                       "weekend_id":weekend_id
                   }
                   weekEndidDist= self.DOT.convert_to_dotdict(weekEndIDObj)
                   weekEndObj= await  self.generalModel.getData(weekEndidDist,"weekendById")

                   if weekEndObj['status']=="success":

                        updateWeekend= await self.generalModel.updateWeekend(weekend_id,weekend_name,day_name_list_id,comments,user_id, user_ip)
                        #print(updateWeekend)
                        if updateWeekend=="success":

                            return {
                                "status": "success",
                                "message": "Your request has been successfully completed.",
                                "data": data
                            }

                        else:
                            return {
                                "status": "error",
                                "message": "Unfortunately, we are unable to process your request at this time. Please contact our support team for assistance.",
                                "data": data
                            }
                   else:
                       return {
                           "status": "error",
                           "message": "Unfortunately, we are unable to process your request at this time. Check your weekend id.",
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



    async def departmentNameList(self, data):
        if data:

            checkIP = await self.checkWhiteIP(data.user_ip)

            if checkIP['status']:

               departmentList= await self.generalModel.getData(data,"departmentNameList")

               return {
                   "status": "success",
                   "message": "The Department name list has been successfully retrieved",
                   "data": departmentList
               }

            else:

                return {
                    "status": "error",
                    "message": checkIP['message'],
                    "data": data
                }
        else:
            return self.mgsLib.default(False)

    async def designationNameList(self, data):
        if data:

            checkIP = await self.checkWhiteIP(data.user_ip)

            if checkIP['status']:

               designationNameList= await self.generalModel.getData(data,"designationNameList")

               return {
                   "status": "success",
                   "message": "The Designation name list has been successfully retrieved",
                   "data": designationNameList
               }

            else:

                return {
                    "status": "error",
                    "message": checkIP['message'],
                    "data": data
                }
        else:
            return self.mgsLib.default(False)

    async def eventNameList(self, data):
        if data:

            checkIP = await self.checkWhiteIP(data.user_ip)

            if checkIP['status']:

               eventNamelist= await self.generalModel.getData(data,"eventNameList")

               return {
                   "status": "success",
                   "message": "The Event name list has been successfully retrieved",
                   "data": eventNamelist
               }

            else:

                return {
                    "status": "error",
                    "message": checkIP['message'],
                    "data": data
                }
        else:
            return self.mgsLib.default(False)

    async def accessIPList(self, data):
        if data:

            checkIP = await self.checkWhiteIP(data.user_ip)

            if checkIP['status']:

                whiteIPList = await self.generalModel.getData(data, "accessIPList")

                return {
                    "status": "success",
                    "message": "The White ip list has been successfully retrieved",
                    "data": whiteIPList
                }

            else:

                return {
                    "status": "error",
                    "message": checkIP['message'],
                    "data": data
                }
        else:
            return self.mgsLib.default(False)


    async def addAccessIPList(self, data):
        if data:

            checkIP = await self.checkWhiteIP(data.user_ip)

            if checkIP['status']:
                checkOfficeId=await  self.generalModel.getOfficeInfoById(data.office_id)
                if checkOfficeId:

                    addWhiteIPList = await self.generalModel.insertData(data, "", "addAccessIPList")

                    if addWhiteIPList["status"] == "success":

                        return {
                            "status": "success",
                            "message": "Your request has been successfully completed.",
                            "data": addWhiteIPList
                        }

                    else:
                        return {
                            "status": "error",
                            "message": "Unfortunately, we are unable to process your request at this time. Please contact our support team for assistance.",
                            "data": data
                        }

                else:
                    return {
                        "status": "error",
                        "message": " Unfortunately, the office ID you entered was not found in our system.",
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

    async def updateAccessIPList(self, data):
        if data:

            checkIP = await self.checkWhiteIP(data.user_ip)

            if checkIP['status']:
                checkAccessIPData = await  self.generalModel.getAccessIPInfoById(data.access_ip_id)
                if checkAccessIPData:

                    updateAccessIP = await self.generalModel.updateAccessIPList(data)

                    if updateAccessIP == "success":

                        return {
                            "status": "success",
                            "message": "Your request has been successfully completed.",
                            "data": data
                        }

                    else:
                        return {
                            "status": "error",
                            "message": "Unfortunately, we are unable to process your request at this time. Please contact our support team for assistance.",
                            "data": data
                        }

                else:
                    return {
                        "status": "error",
                        "message": " Unfortunately, the access ip id you entered that was not found in our system.",
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


    async def officeList(self, data):
        if data:

            checkIP = await self.checkWhiteIP(data.user_ip)

            if checkIP['status']:

                officeList = await self.generalModel.getData(data, "officeList")

                return {
                    "status": "success",
                    "message": "The office list has been successfully retrieved",
                    "data": officeList
                }

            else:

                return {
                    "status": "error",
                    "message": checkIP['message'],
                    "data": data
                }
        else:
            return self.mgsLib.default(False)


    async def addNewOfficeInformation(self, data):
        if data:

            checkIP = await self.checkWhiteIP(data.user_ip)

            if checkIP['status']:

                isOrganization_name = await self.validation.isSQLInjectionContent(data.organization_name)
                isAddress = await self.validation.isSQLInjectionContent(data.address)
                isComments = await self.validation.isSQLInjectionContent(data.comments)

                #print(isOrganization_name,"--->",isComments)
                if isOrganization_name or isAddress or isComments:
                    return self.mgsLib.default("sql")
                else:
                    addOfficeData=await self.generalModel.insertData(data,"","addNewOfficeInformation")
                    if addOfficeData['status']=="success":
                        edata={
                            "insert_data":data,
                            "inserted_id":addOfficeData['data']
                        }
                        return self.mgsLib.insertMessage("success",False,edata)
                    else:
                        return self.mgsLib.insertMessage(addOfficeData['status'], False, data)


            else:

                return {
                    "status": "error",
                    "message": checkIP['message'],
                    "data": data
                }
        else:
            return self.mgsLib.default(False)

    async def updateOfficeInformation(self, data):
        if data:

            checkIP = await self.checkWhiteIP(data.user_ip)

            if checkIP['status']:

                isOrganization_name = await self.validation.isSQLInjectionContent(data.organization_name)
                isAddress = await self.validation.isSQLInjectionContent(data.address)
                isComments = await self.validation.isSQLInjectionContent(data.comments)

                # print(isOrganization_name,"--->",isComments)
                if isOrganization_name or isAddress or isComments:
                    return self.mgsLib.default("sql")
                else:

                    checkOfficeID=await self.generalModel.getOfficeInfoById(data.office_id)

                    if checkOfficeID:
                        updateActionData= await self.generalModel.updateOfficeInformation(data)

                        return self.mgsLib.updateMessage(updateActionData,False,data)


                    else:
                        return {
                            "status": "error",
                            "message": " Unfortunately, the office id you entered that was not found in our system.",
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


# user config----------------------------------------------------

    async def userConfigList(self, data):
        if data:

            checkIP = await self.checkWhiteIP(data.user_ip)

            if checkIP['status']:

                userConfigList = await self.generalModel.getData(data, "userConfigList")
                if userConfigList['status']=="success":
                    return {
                        "status": "success",
                        "message": "The office list has been successfully retrieved",
                        "data": userConfigList
                    }
                else:
                    return self.mgsLib.getMessage(userConfigList['status'],False,data)

            else:

                return {
                    "status": "error",
                    "message": checkIP['message'],
                    "data": data
                }
        else:
            return self.mgsLib.default(False)


    async def addUserConfig(self, data):
        if data:

            checkIP = await self.checkWhiteIP(data.user_ip)

            if checkIP['status']:

                isComments = await self.validation.isSQLInjectionContent(data.comments)

                #print(isOrganization_name,"--->",isComments)
                if isComments:
                    return self.mgsLib.default("sql")
                else:
                    addUserConfigData=await self.generalModel.insertData(data,"","addUserConfig")
                    if addUserConfigData['status']=="success":
                        edata={
                            "insert_data":data,
                            "inserted_id":addUserConfigData['data']
                        }
                        return self.mgsLib.insertMessage("success",False,edata)
                    else:
                        return self.mgsLib.insertMessage(addUserConfigData['status'], False, data)


            else:

                return {
                    "status": "error",
                    "message": checkIP['message'],
                    "data": data
                }
        else:
            return self.mgsLib.default(False)

    async def updateUserConfig(self, data):
        if data:

            checkIP = await self.checkWhiteIP(data.user_ip)

            if checkIP['status']:


                isComments = await self.validation.isSQLInjectionContent(data.comments)

                # print(isOrganization_name,"--->",isComments)
                if isComments:
                    return self.mgsLib.default("sql")
                else:

                    checkUserConfigID=await self.generalModel.getUserConfigInfoById(data.user_config_id)

                    if checkUserConfigID:
                        updateActionData= await self.generalModel.updateUserConfig(data)

                        return self.mgsLib.updateMessage(updateActionData,False,data)
                    else:
                        return {
                            "status": "error",
                            "message": " Unfortunately, the userConfig id you entered that was not found in our system.",
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



# holiday setup ----------------------------------------------------

    async def holidayList(self, data):
        if data:

            checkIP = await self.checkWhiteIP(data.user_ip)

            if checkIP['status']:

                holidayList = await self.generalModel.getData(data, "holidayList")
                if holidayList['status']=="success":
                    return {
                        "status": "success",
                        "message": "The office list has been successfully retrieved",
                        "data": holidayList
                    }
                else:
                    return self.mgsLib.getMessage(holidayList['status'],False,data)

            else:

                return {
                    "status": "error",
                    "message": checkIP['message'],
                    "data": data
                }
        else:
            return self.mgsLib.default(False)


    async def addHolidayList(self, data):
        if data:

            checkIP = await self.checkWhiteIP(data.user_ip)

            if checkIP['status']:

                isComments = await self.validation.isSQLInjectionContent(data.comments)

                #print(isOrganization_name,"--->",isComments)
                if isComments:
                    return self.mgsLib.default("sql")
                else:
                    checkAlready=await  self.generalModel.getData(data,"isAlreadyExist")

                    if checkAlready['status']=="notExist":
                        addHolidayList = await self.generalModel.insertData(data, "", "addHolidayList")

                        if addHolidayList['status'] == "success":
                            edata = {
                                "insert_data": data,
                                "inserted_id": addHolidayList['data']
                            }
                            return self.mgsLib.insertMessage("success", False, edata)
                        else:
                            return self.mgsLib.insertMessage(addHolidayList['status'], False, data)
                    else:
                        return self.mgsLib.getMessage("exist",False,data)

            else:

                return {
                    "status": "error",
                    "message": checkIP['message'],
                    "data": data
                }
        else:
            return self.mgsLib.default(False)

    async def updateHolidayList(self, data):
        if data:

            checkIP = await self.checkWhiteIP(data.user_ip)

            if checkIP['status']:


                isComments = await self.validation.isSQLInjectionContent(data.comments)

                # print(isOrganization_name,"--->",isComments)
                if isComments:
                    return self.mgsLib.default("sql")
                else:

                    checkHolidayData=await self.generalModel.holidayInfoById(data.office_holiday_config_id)

                    if checkHolidayData:
                        updateActionData= await self.generalModel.updateHolidayList(data)

                        return self.mgsLib.updateMessage(updateActionData,False,data)
                    else:
                        return {
                            "status": "error",
                            "message": " Unfortunately, the office holiday config id you entered that was not found in our system.",
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
