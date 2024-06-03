# authController
from models.authModel import AuthModel
from models.generalModel import GeneralModel
from models.eventModel import EventModel
from libraries.message import Message
from libraries.frz import  Frz
from libraries.validation import  Validation
from libraries.password import Password
from libraries.jsonFormate import JsonFormate
from libraries.dotDict import DotDict
from libraries.evement_management import EventManagement

class ReportController:
    def __init__(self):
        self.authModel = AuthModel()
        self.generalModel = GeneralModel()
        self.eventModel = EventModel()

        self.authModel = AuthModel()
        self.mgsLib = Message()
        self.Frz = Frz()
        self.validation = Validation()
        self.PSW = Password()
        self.JSON = JsonFormate()
        self.DOT = DotDict()
        self.Event = EventManagement()

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

    async def showReport(self, data):
        if data:

            checkIP = await self.checkWhiteIP(data.user_ip)

            if checkIP['status'] == True:

                isFromDateValidation = await self.Frz.isDateFormate(data.from_date)
                isToDateValidation = await self.Frz.isDateFormate(data.to_date)

                #print(isFromDateValidation,"----------------------", isToDateValidation)

                if isFromDateValidation == True and isToDateValidation == True:

                    utcData = await self.authModel.getUserTTSConfigInformation(data.user_id)
                    utcDbData = self.JSON.getDecodedData(utcData).get('data')

                    reportData = await self.reportGenerate(data,utcDbData)



                    if reportData == False:
                        return {
                            "status": "success",
                            "message": " During the specified search date range, there are no available information.",
                            "data": False
                        }
                    else:
                        # working...
                        #print(reportData)
                        return {
                            "status": "success",
                            "message": "Your request successfully done",
                            "data": reportData
                        }
                else:
                    return self.mgsLib.isValidInputMgs("error", data)

            else:

                return {
                    "status": "error",
                    "message": checkIP['message'],
                    "data": data
                }
        else:
            return self.mgsLib.default(False)
    async def reportGenerate(self,data,utcDbData):
        #type[date,day,month,year]

        eventData = await self.eventModel.showEventInformation(data.user_id, data.from_date, data.to_date, utcDbData)
        #array_size = len(eventData['total_month_data'])
        #print(eventData)

        if eventData:
                return [eventData]
        else:
            return False




