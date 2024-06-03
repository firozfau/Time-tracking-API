# eventController
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

class EventController:
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



  # eventAction is main method of event
    async def eventAction(self, data):
        if data:

            checkIP = await self.checkWhiteIP(data.user_ip)

            if checkIP['status']:

                isToken= await self.validation.isSQLInjectionContent(data.sessionToken)
                isComments = await self.validation.isSQLInjectionContent(data.comments)

                if isToken or isComments:
                    return self.mgsLib.default("sql")
                else:

                    verifyToken= await self.authModel.activeLoginHistoryTokenId(data.sessionToken,data.user_id)

                    # token is verified...
                    if verifyToken:

                        utcData = await self.authModel.getUserTTSConfigInformation(data.user_id)
                        utcDbData = self.JSON.getDecodedData(utcData).get('data')
                        verifyTokenLoginData = self.JSON.getDecodedData(verifyToken).get('data')
                        user_utc_current_date = await self.Frz.getDateTimeByUTC(int(utcDbData['time_zone']), True)
                        isValidLoinSession=await self.Event.isValidLoinSession(verifyTokenLoginData['user_utc_login_time'],user_utc_current_date)
                        lastArrivalEvent = await self.eventModel.getLastArrivalEvent(data.user_id)
                        isArrivalRequest= self.Event.isArrivalRequest(data.event_name_id)

                        if isValidLoinSession:

                            if lastArrivalEvent:

                                lastArrivalEventObj = self.JSON.getDecodedData(lastArrivalEvent)
                                last_arrival_user_utc_time = lastArrivalEventObj['data']['event_start_user_utc_date_time']
                                lastEventDataByDate =await self.eventModel.getAllEventDataByDate(data.user_id,last_arrival_user_utc_time)

                                last_arrival_day_start_time=await self.Event.getMinimumHoursDateTime(last_arrival_user_utc_time)
                                isWorkTimeAvailable = await self.Event.isWorkTimeAvailable(last_arrival_day_start_time, user_utc_current_date)
                                isArrivalDateIsRunning = await self.Event.isSameDate(last_arrival_user_utc_time, user_utc_current_date)



                                if lastEventDataByDate:


                                   isValidRequest = await self.Event.isValidRequest(lastEventDataByDate, data.event_name_id)


                                   if isArrivalDateIsRunning ==True:
                                        isDeparture = await self.eventModel.isDeparture(data.user_id, user_utc_current_date)

                                        if isDeparture==True:
                                            return self.mgsLib.getEventMessage("invalidRequest", data)
                                        else:

                                            if isWorkTimeAvailable==True:
                                                isExistEvent = await self.eventModel.isExistEventByEventData(lastEventDataByDate,data.event_name_id)
                                                if isExistEvent==True:
                                                    return self.mgsLib.getEventMessage("invalidRequest", data)
                                                else:
                                                    if isValidRequest==True:
                                                        result = await self.insertEventData(data, user_utc_current_date,1)
                                                        if result:
                                                            return self.mgsLib.getEventMessage("success", data)
                                                        else:
                                                            return self.mgsLib.getEventMessage("error", data)
                                                    else:
                                                        return self.mgsLib.getEventMessage("invalidRequest", data)

                                            else:
                                                departureResult= await self.requestSystemDeparture(data, user_utc_current_date,last_arrival_user_utc_time)
                                                if departureResult==True:
                                                    if self.Event.isArrivalRequest(data.event_name_id):
                                                        return self.mgsLib.getEventMessage("error", data)
                                                    else:
                                                        return self.mgsLib.getEventMessage("needArrival", data)
                                                else:
                                                    return self.mgsLib.getEventMessage("error", data)
                                   else:

                                       isDeparture = await self.eventModel.isDeparture(data.user_id,last_arrival_user_utc_time)

                                       if isDeparture == True:
                                           # today new event
                                           todayEventDataByDate = await self.eventModel.getAllEventDataByDate(data.user_id, user_utc_current_date)

                                           if todayEventDataByDate:
                                               isValidRequest = await self.Event.isValidRequest(todayEventDataByDate,data.event_name_id)

                                               if isValidRequest == True:
                                                   result = await self.insertEventData(data, user_utc_current_date, 1)
                                                   if result:
                                                       return self.mgsLib.getEventMessage("success", data)
                                                   else:
                                                       return self.mgsLib.getEventMessage("error", data)
                                               else:
                                                   return self.mgsLib.getEventMessage("invalidRequest", data)
                                           else:
                                               isArrivalRequest = self.Event.isArrivalRequest(data.event_name_id)
                                               if isArrivalRequest:
                                                   result = await self.insertEventData(data, user_utc_current_date, 1)
                                                   if result:
                                                       return self.mgsLib.getEventMessage("success", data)
                                                   else:
                                                       return self.mgsLib.getEventMessage("error", data)
                                               else:
                                                   return self.mgsLib.getEventMessage("invalidRequest", data)

                                       else:
                                           departureResult = await self.requestSystemDeparture(data,
                                                                                               user_utc_current_date,
                                                                                               last_arrival_user_utc_time)
                                           if departureResult == True:
                                               if self.Event.isArrivalRequest(data.event_name_id):
                                                   return self.mgsLib.getEventMessage("error", data)
                                               else:
                                                   return self.mgsLib.getEventMessage("needArrival", data)
                                           else:
                                               return self.mgsLib.getEventMessage("error", data)
                                else:
                                    return self.mgsLib.getEventMessage("error", data)
                            else:

                                if isArrivalRequest:
                                    result = await self.insertEventData(data, user_utc_current_date,1)
                                    if result:
                                        return self.mgsLib.getEventMessage("success", data)
                                    else:
                                        return self.mgsLib.getEventMessage("error", data)
                                else:
                                    return self.mgsLib.getEventMessage("needArrival", data)


                        else:

                            comments = "system auto log out "
                            logoutData=await self.authModel.userLoginUpdate(data.user_id, user_utc_current_date, 2, comments)

                            return self.mgsLib.getEventMessage("sessionTimeout", data)


                    else:
                        return self.mgsLib.getEventMessage("invalidToken",data)



            else:

                return {
                    "status": "error",
                    "message": checkIP['message'],
                    "data": data
                }
        else:
            return self.mgsLib.default(False)



    async def insertEventData(self,data,action_user_utc_date_time,event_action_type):

        optionNalObj = {
            "action_user_utc_date_time": action_user_utc_date_time,
            "event_action_type":event_action_type,
        }
        insertData = await self.eventModel.insertData(data, optionNalObj,"addEvent")
        if insertData['status'] == "success":
            await  self.eventEmailNotification( action_user_utc_date_time, data)
            return True
        else:
            return False

    async def requestSystemDeparture(self,data,action_user_utc_date_time,arrival_user_utc_date_time):
        isDeparture=await self.eventModel.isDeparture(data.user_id,arrival_user_utc_date_time)
        if isDeparture:
            return True
        else:
            comments="System make auto departure"
            event_action_type=2
            optionNalObj = {
                "comments": comments,
                "user_id": data.user_id,
                "action_user_utc_date_time":await self.Event.getMaxEightHours(arrival_user_utc_date_time),
                "event_action_type":event_action_type,
                "event_start_ip": data.user_id,
                "auto_departure_user_utc_date_time":action_user_utc_date_time
            }

            insertData = await self.eventModel.insertData(data, optionNalObj,"systemDeparture")
            if insertData['status'] == "success":
                await  self.eventEmailNotification(action_user_utc_date_time, data, True)
                return True
            else:
                return False







    #Check any active event
    async def activeEvent(self, data):
        if data:

            checkIP = await self.checkWhiteIP(data.user_ip)

            if checkIP['status']:

                isToken = await self.validation.isSQLInjectionContent(data.sessionToken)
                if isToken:
                    return self.mgsLib.default("sql")
                else:

                    verifyToken = await self.authModel.activeLoginHistoryTokenId(data.sessionToken, data.user_id)
                    # token is verified...
                    if verifyToken:

                        utcData = await self.authModel.getUserTTSConfigInformation(data.user_id)

                        utcDbData = self.JSON.getDecodedData(utcData).get('data')
                        verifyTokenLoginData = self.JSON.getDecodedData(verifyToken).get('data')
                        user_utc_current_date = await self.Frz.getDateTimeByUTC(int(utcDbData['time_zone']), True)
                        isValidLoinSession = await self.Event.isValidLoinSession(
                        verifyTokenLoginData['user_utc_login_time'], user_utc_current_date)
                        lastArrivalEvent = await self.eventModel.getLastArrivalEvent(data.user_id)


                        if isValidLoinSession:

                            if lastArrivalEvent:

                                lastArrivalEventObj = self.JSON.getDecodedData(lastArrivalEvent)
                                last_arrival_user_utc_time = lastArrivalEventObj['data']['event_start_user_utc_date_time']
                                lastEventDataByDate =await self.eventModel.getAllEventDataByDate(data.user_id,last_arrival_user_utc_time)

                                last_arrival_day_start_time = await self.Event.getMinimumHoursDateTime(last_arrival_user_utc_time)
                                isWorkTimeAvailable = await self.Event.isWorkTimeAvailable(last_arrival_day_start_time, user_utc_current_date)
                                isArrivalDateIsRunning = await self.Event.isSameDate(last_arrival_user_utc_time, user_utc_current_date)


                                if lastEventDataByDate:
                                   isDeparture = await self.eventModel.isDeparture(data.user_id,last_arrival_user_utc_time)
                                   #print(isArrivalDateIsRunning,"------_",isDeparture,"_------",last_arrival_user_utc_time)

                                   if isArrivalDateIsRunning ==True:



                                        if isDeparture==True:
                                            event_list_object = await self.eventModel.getEventListObjectList("dayClosed")
                                            return self.mgsLib.getEventMessage("success", event_list_object)
                                        else:

                                            if isWorkTimeAvailable==True:
                                                #check which list is perfect
                                                event_list_object = await self.eventModel.getEventListObjectList(lastEventDataByDate)
                                                #print("-->", event_list_object)
                                                return self.mgsLib.getEventMessage("success", event_list_object)

                                            else:

                                                departureResult = await self.requestSystemDeparture(data,user_utc_current_date,last_arrival_user_utc_time)
                                                #print("-->", departureResult)
                                                if departureResult == True:
                                                    event_list_object = await self.eventModel.getEventListObjectList("dayClosed")
                                                    return self.mgsLib.getEventMessage("success", event_list_object)
                                                else:
                                                    return self.mgsLib.getEventMessage("error", data)

                                   else:

                                       if isDeparture == True:

                                           event_list_object = await self.eventModel.getEventListObjectList()

                                           return self.mgsLib.getEventMessage("success", event_list_object)
                                       else:
                                           departureResult = await self.requestSystemDeparture(data,
                                                                                               user_utc_current_date,
                                                                                               last_arrival_user_utc_time)
                                           if departureResult == True:
                                               event_list_object = await self.eventModel.getEventListObjectList()
                                               return self.mgsLib.getEventMessage("success", event_list_object)
                                           else:
                                               return self.mgsLib.getEventMessage("error", data)

                                else:
                                    return self.mgsLib.getEventMessage("error", data)


                            else:
                               event_list_object=await self.eventModel.getEventListObjectList()

                               return self.mgsLib.getEventMessage("success", event_list_object)
                        else:

                            comments = "system auto log out"
                            logoutData = await self.authModel.userLoginUpdate(data.user_id, user_utc_current_date, 2,
                                                                              comments)

                            return self.mgsLib.getEventMessage("sessionTimeout", data)
                    else:
                        return self.mgsLib.getEventMessage("invalidToken", data)



            else:

                return {
                    "status": "error",
                    "message": checkIP['message'],
                    "data": data
                }
        else:
            return self.mgsLib.default(False)

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


    async def showEventInformation(self, data):
        if data:

            checkIP = await self.checkWhiteIP(data.user_ip)

            if checkIP['status']==True:

                isFromDateValidation=await self.Frz.isDateFormate(data.from_date)
                isToDateValidation = await self.Frz.isDateFormate(data.to_date)
                if isFromDateValidation ==True and isToDateValidation==True:

                    utcData = await self.authModel.getUserTTSConfigInformation(data.user_id)
                    utcDbData = self.JSON.getDecodedData(utcData).get('data')


                    eventData=await self.eventModel.showEventInformation(data.user_id,data.from_date,data.to_date,utcDbData)
                    if eventData==False:
                        return {
                                "status": "success",
                                "message": " During the specified search date range, there are no available events.",
                                "data": False
                            }
                    else:
                        return {
                            "status": "success",
                            "message": " During the specified search date range, there are no available events.",
                            "data": eventData
                        }
                else:
                    return self.mgsLib.isValidInputMgs("error",data)

            else:

                return {
                    "status": "error",
                    "message": checkIP['message'],
                    "data": data
                }
        else:
            return self.mgsLib.default(False)

    async def eventEmailNotification(self,action_user_utc_date_time, data, isAutoDeparture=False):
        from libraries.mailbox import Mailbox
        Mail = Mailbox()

        from pprint import pprint

        action_date_formate= await Mail.daYofDateFormate(action_user_utc_date_time)
        accountData = await  self.authModel.byUserOpenKey(data.user_id, "id")

        if accountData:
            accountObjectData = self.JSON.getDecodedData(accountData)['data']

            # 2024-05-29 08:14:45 PM
            utcData = await self.authModel.getUserTTSConfigInformation(data.user_id)
            utcDbData = self.JSON.getDecodedData(utcData).get('data')

            from_date = action_user_utc_date_time
            to_date = action_user_utc_date_time
            eventData = await self.eventModel.showEventInformation(data.user_id, from_date, to_date, utcDbData)


            if eventData == False:
                from_date = await Mail.subtractOneDay(from_date)
                eventData = await self.eventModel.showEventInformation(data.user_id, from_date, to_date, utcDbData)

            required_data = eventData['required_data']

            total_spend_working_time = await Mail.minutes_to_time(required_data['total_spend_working_time'])
            total_actual_working_time = await Mail.minutes_to_time(required_data['total_actual_working_time'])

            isEarlyDeparture=await Mail.isEarlyDeparture(required_data['total_actual_working_time'])

            keywordDate = await Mail.dateFormate(to_date)
            main_data = required_data[keywordDate]
            basic_info = main_data['basic_info']
            workHistory = main_data['data']

            default_work_start_time = basic_info['default_work_start_time']
            default_work_end_time = basic_info['default_work_end_time']

            arrival_date_time = basic_info['arrival_date_time']
            departure_date_time = basic_info['departure_date_time']

            arrival_comments = basic_info['arrival_comments']


            if isAutoDeparture or data.event_name_id == 2:

                email_subject=await Mail.eventMailContent("d")
                full_name = accountObjectData['first_name']+" "+accountObjectData['last_name']

                mailObject = {
                    'to_email': accountObjectData['email'],
                    'subject': email_subject,
                    'full_name': full_name,
                    'notify_time': action_date_formate,
                    'total_spend_working_time': total_spend_working_time,
                    'total_actual_working_time': total_actual_working_time,
                    'workHistory': workHistory

                }

                result = await Mail.eventEmail("d", mailObject)

                if isAutoDeparture:
                    mailObject['subject'] = await Mail.eventMailContent("misD")
                    result = await Mail.eventEmail("misD", mailObject)


                else:
                    if isEarlyDeparture:
                        mailObject['subject'] = await Mail.eventMailContent("ed")
                        mailObject['notify_time'] =isEarlyDeparture


                        result = await Mail.eventEmail("ed", mailObject)




            elif data.event_name_id ==1 :
                isLate= await Mail.isLateArrival(default_work_start_time,arrival_date_time)
                if isLate:
                    email_subject = await Mail.eventMailContent("la")
                    full_name = accountObjectData['first_name'] + " " + accountObjectData['last_name']

                    mailObject = {
                        'to_email': accountObjectData['email'],
                        'subject': email_subject,
                        'full_name': full_name,
                        'notify_time': arrival_comments,
                        'actionDate':action_date_formate

                    }

                    result = await Mail.eventEmail("la", mailObject)



