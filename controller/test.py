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
                        current_date_time=await self.Frz.getCurrentDateTime()
                        user_utc_current_date = await self.Frz.getDateTimeByUTC(int(utcDbData['time_zone']), True)

                        isValidLoinSession=await self.Event.isValidLoinSession(verifyTokenLoginData['user_utc_login_time'],user_utc_current_date)


                        if isValidLoinSession:

                            lastArrivalEvent=await self.eventModel.getLastArrivalEvent(data.user_id)

                            #print(lastArrivalEvent, "--->", user_utc_current_date)
                            #return lastArrivalEvent

                            if lastArrivalEvent:


                                lastArrivalEventObj= self.JSON.getDecodedData(lastArrivalEvent)
                                last_arrival_user_utc_time=lastArrivalEventObj['data']['event_start_user_utc_date_time']
                                isArrivalDateIsRunning = await self.Event.isSameDate(last_arrival_user_utc_time,user_utc_current_date)

                                if isArrivalDateIsRunning:

                                    isWorkTimeAvailable = await self.Event.isWorkTimeAvailable(last_arrival_user_utc_time,user_utc_current_date)
                                    if isWorkTimeAvailable:
                                        isDepartureDone = await self.eventModel.isDepartureDone(data.user_id,user_utc_current_date)
                                        isRequestedEventExist= await self.eventModel.isRequestedEventExist(data.user_id,data.event_name_id,data.status,user_utc_current_date)

                                        if isRequestedEventExist:
                                            return self.mgsLib.getEventMessage("exist",data)
                                        elif isDepartureDone:
                                            return self.mgsLib.getEventMessage("invalidRequest", data)
                                        else:

                                            isArrivalDone = await self.eventModel.isArrivalDone(data.user_id,user_utc_current_date)
                                            isBaseRequestDone = await self.eventModel.isRequestedEventExist(data.user_id, data.event_name_id, 1, user_utc_current_date)
                                            departureId=await self.Event.getDepartureEventId()

                                            isAnyEventActiveExceptAD=await self.eventModel.isAnyEventActiveExceptAD(data.user_id,user_utc_current_date)

                                            if isArrivalDone==False and data.event_name_id == departureId:
                                                return self.mgsLib.getEventMessage("needArrival", data)
                                            if data.status==2 and  isBaseRequestDone== False:
                                                return self.mgsLib.getEventMessage("invalidRequest", data)
                                            if data.status == 2 and data.event_name_id == departureId:
                                                return self.mgsLib.getEventMessage("invalidRequest", data)
                                            if data.status == 1 and isAnyEventActiveExceptAD:
                                                return self.mgsLib.getEventMessage("invalidRequest", data)
                                            else:

                                                if data.status==1:
                                                    # create new event
                                                    result = await self.insertEventData(data, user_utc_current_date)
                                                    if result:
                                                        return self.mgsLib.getEventMessage("success", data)
                                                    else:
                                                        return self.mgsLib.getEventMessage("error", data)
                                                else:
                                                    # update manual event
                                                    result =await self.updateEventData(data,user_utc_current_date)
                                                    if result:
                                                        return self.mgsLib.getEventMessage("success", data)
                                                    else:
                                                        return self.mgsLib.getEventMessage("error", data)



                                    else:
                                        # arrival and current is not same , it is time over show just update pending request and request for new new arrival

                                        result = await self.updatePendingEventData(data, last_arrival_user_utc_time, user_utc_current_date)
                                        if result:
                                            return self.mgsLib.getEventMessage("needArrival", data)
                                        else:
                                            return self.mgsLib.getEventMessage("error", data)

                                else:
                                    # arrival and current is not same , it is time over show just update pending request and request for new new arrival

                                    isMissingEventDone = await self.eventModel.isMissingEventDone(data.user_id,last_arrival_user_utc_time,user_utc_current_date)
                                    isArrivalRequest=await self.Event.isArrivalRequest(data.event_name_id)

                                    if isMissingEventDone:

                                        if isArrivalRequest:
                                            result = await self.insertEventData(data, user_utc_current_date)
                                            if result:
                                                return self.mgsLib.getEventMessage("success", data)
                                            else:
                                                return self.mgsLib.getEventMessage("error", data)
                                        else:
                                            return self.mgsLib.getEventMessage("needArrival", data)
                                    else:
                                        result= await self.updatePendingEventData(data,last_arrival_user_utc_time,user_utc_current_date)
                                        if result:
                                            return self.mgsLib.getEventMessage("needArrival", data)
                                        else:
                                            return self.mgsLib.getEventMessage("error", data)


                            else:
                                isDayClosed=await self.eventModel.isDayClosed(data.user_id,user_utc_current_date)
                                isRequestedEventExist =await self.eventModel.isRequestedEventExist(data.user_id, data.event_name_id, data.status,user_utc_current_date)

                                isArrivalDone = await self.eventModel.isArrivalDone(data.user_id, user_utc_current_date)
                                isArrivalEventID=await self.Event.getArrivalEventId()


                                if isDayClosed:
                                    return self.mgsLib.getEventMessage("invalidRequest", data)
                                elif isRequestedEventExist:
                                    return self.mgsLib.getEventMessage("exist", data)
                                elif data.event_name_id!=isArrivalEventID:
                                    return self.mgsLib.getEventMessage("invalidRequest", data)
                                elif data.status!=1:
                                    return self.mgsLib.getEventMessage("invalidRequest", data)
                                else:
                                    # call insert event
                                    if isArrivalDone == False:
                                       result=await self.insertEventData(data,user_utc_current_date)
                                       if result:
                                           return self.mgsLib.getEventMessage("success", data)
                                       else:
                                           return self.mgsLib.getEventMessage("error", data)
                                    else:
                                        return self.mgsLib.getEventMessage("needArrival", data)

                        else:

                            comments = "system auto log out due to day over"
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



    async def insertEventData(self,data,action_user_utc_date_time):

        optionNalObj = {
            "action_user_utc_date_time": action_user_utc_date_time
        }
        insertData = await self.eventModel.insertData(data, optionNalObj,"addEvent")
        if insertData['status'] == "success":
            return True
        else:
            return False

    async def updateEventData(self,data,user_utc_current_date):

        lastActiveEventData=await self.eventModel.getLastActiveEvent(data.user_id)
        if lastActiveEventData:

            lastArrivalEventObj =  self.JSON.getDecodedData(lastActiveEventData).get('data')


            extra_data = {
                "lunch_break": await self.eventModel.isLunchBreakDone(data.user_id, user_utc_current_date)
            }
            event_update_data = await self.Event.eventStatusInnerDay(lastArrivalEventObj['event_name_id'], extra_data)

            update_event_object = {
                "event_action_type": event_update_data['event_action_type'],
                "is_missing_event": event_update_data['is_missing_event'],
                "event_penalty_id": event_update_data['event_penalty_id'],
                "missing_event_information": event_update_data[ 'missing_event_information'],
                "status": 2,
                "comments":  data.comments,
                "event_end_date_time": await self.Frz.getCurrentDateTime(),
                "event_end_user_utc_date_time": user_utc_current_date,

                "event_end_ip": data.user_ip,
                "id": lastArrivalEventObj['id']
            }
            pendingEventUpdateResult = await self.eventModel.updateEvent( update_event_object)
            if pendingEventUpdateResult == "success":
                return True
            else:
                return False

        else:
            return False
    async def updatePendingEventData(self,data,last_arrival_user_utc_time,user_utc_current_date):

        lastActiveEventData=await self.eventModel.getLastActiveEvent(data.user_id)


        if lastActiveEventData:

            lastArrivalEventObj =  self.JSON.getDecodedData(lastActiveEventData).get('data')


            extra_data = {
                "lunch_break": await self.eventModel.isLunchBreakDone(data.user_id, last_arrival_user_utc_time)
            }
            event_update_data = await self.Event.eventStatusDayOver(lastArrivalEventObj['event_name_id'], extra_data)

            update_event_object = {
                "event_action_type": event_update_data['event_action_type'],
                "is_missing_event": event_update_data['is_missing_event'],
                "event_penalty_id": event_update_data['event_penalty_id'],
                "missing_event_information": event_update_data[ 'missing_event_information'],
                "status": 2,
                "comments": "Auto closed day event user UTC date is " + user_utc_current_date,
                "event_end_date_time": "00:00:00.000000",
                "event_end_user_utc_date_time": "00:00:00.000000",
                "event_end_ip": data.user_ip,
                "id": lastArrivalEventObj['id']
            }

            pendingEventUpdateResult = await self.eventModel.updateEvent( update_event_object)
            if pendingEventUpdateResult == "success":
                return True
            else:
                return False

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
                        current_date_time = await self.Frz.getCurrentDateTime()
                        user_utc_current_date = await self.Frz.getDateTimeByUTC(int(utcDbData['time_zone']), True)

                        isValidLoinSession = await self.Event.isValidLoinSession(
                            verifyTokenLoginData['user_utc_login_time'], user_utc_current_date)

                        if isValidLoinSession:

                            lastArrivalEvent = await self.eventModel.getLastArrivalEvent(data.user_id)

                            if lastArrivalEvent:

                                lastArrivalEventObj = self.JSON.getDecodedData(lastArrivalEvent)
                                last_arrival_user_utc_time = lastArrivalEventObj['data']['event_start_user_utc_date_time']
                                isArrivalDateIsRunning = await self.Event.isSameDate(last_arrival_user_utc_time, user_utc_current_date)
                                isMissingEventDone = await self.eventModel.isMissingEventDone(data.user_id,last_arrival_user_utc_time,user_utc_current_date)
                                #print(last_arrival_user_utc_time,"--->",user_utc_current_date)
                                #return isArrivalDateIsRunning
                                if isArrivalDateIsRunning:

                                    isWorkTimeAvailable = await self.Event.isWorkTimeAvailable(last_arrival_user_utc_time, user_utc_current_date)
                                    if isWorkTimeAvailable:
                                        return await self.eventModel.getCurrentEventList(data.user_id, user_utc_current_date)
                                    else:
                                        # arrival and current is not same , it is time over show just update pending request and request for  new arrival
                                        if isMissingEventDone:
                                            return await self.eventModel.getCurrentEventList(data.user_id,
                                                                                             user_utc_current_date)
                                        else:
                                            result = await self.updatePendingEventData(data, last_arrival_user_utc_time,
                                                                                       user_utc_current_date)
                                            if result:
                                                return await self.eventModel.getCurrentEventList(data.user_id,
                                                                                                 user_utc_current_date)
                                            else:
                                                return self.mgsLib.getEventMessage("error", data)

                                else:


                                    # arrival and current is not same , it is time over show just update pending request and request for  new arrival
                                    if isMissingEventDone:
                                        return await self.eventModel.getCurrentEventList(data.user_id, user_utc_current_date)
                                    else:
                                        result = await self.updatePendingEventData(data, last_arrival_user_utc_time, user_utc_current_date)
                                        if result:
                                            return await self.eventModel.getCurrentEventList(data.user_id, user_utc_current_date)
                                        else:
                                            return self.mgsLib.getEventMessage("error", data)


                            else:
                                # return event list
                                return await self.eventModel.getCurrentEventList(data.user_id, user_utc_current_date)


                        else:

                            comments = "system auto log out due to day over"
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

                    eventData=await self.eventModel.showEventInformation(data.user_id,data.from_date,data.to_date)
                    if eventData==False:
                        return {
                                "status": "success",
                                "message": " During the specified search date range, there are no available events.",
                                "data": False
                            }
                    else:
                        # not finish work please in model
                        return eventData
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