#eventModel.py
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text
from dbConnection.dbcon import SessionLocal
from libraries.jsonFormate import JsonFormate
from libraries.frz import  Frz
from libraries.evement_management import EventManagement
class EventModel:
    def __init__(self):
        self.DB = SessionLocal()
        self.JSON = JsonFormate()
        self.Frz = Frz()
        self.Event = EventManagement()


    async def fetchData(self, result, data):
        mergeData = [
            dict(zip(result.keys(), row))
            for row in data
        ]
        return mergeData

    async def getData(self, data,methodName):
        try:

            # Begin transaction
            requestMethod = getattr(self, methodName)  # Get the method reference based on methodName
            resultData = await requestMethod(data)  # Call the method with data



            if resultData:  # Checking if any data is fetched
                return {
                    "status": "success",
                    "data":   resultData
                }
            else:
                return {
                    "status":"notExist",
                    "data":False
                }

        except IntegrityError as e:

            return {
                "status": "failed",
                "data": False
            }

        except Exception as e:

            #print(f"Error: {e}")
            return {
                "status": "error",
                "data": False
            }

        finally:
            self.DB.close()


    async def insertData(self, data,optional_object,methodName):
        try:


            # Begin transaction
            #self.DB.begin()


            requestMethod = getattr(self, methodName)  # Get the method reference based on methodName
            resultData = await requestMethod(data,optional_object)  # Call the method with data

            self.DB.commit()

            if resultData:  # Checking if any data is fetched
                return {
                    "status": "success",
                    "data":   resultData
                }
            else:
                return {
                    "status":"failed",
                    "data":False
                }

        except IntegrityError as e:
            self.DB.rollback()
            #print(f"Error: {e}")
            return {
                "status": "failed",
                "data": False
            }

        except Exception as e:
            self.DB.rollback()
            print(f"Error: {e}")
            return {
                "status": "error",
                "data": False
            }

        finally:
            self.DB.close()

    async def addEvent(self, data, objectData):

        sqlQuery = text(
            """
            INSERT INTO daily_events (`user_id`,`event_name_id`,`status`,`comments`,`event_start_ip`, `event_start_user_utc_date_time`)
            VALUES (:user_id, :event_name_id, :status, :comments, :event_start_ip, :event_start_user_utc_date_time)
            """
        )
        result = self.DB.execute(sqlQuery,
                                 {
                                      "user_id": data.user_id,
                                      "event_name_id":data.event_name_id,
                                      "status": data.status,
                                      "comments": data.comments,
                                      "event_start_ip": data.user_ip,
                                     "event_start_user_utc_date_time":objectData['action_user_utc_date_time']

                                 }
                                 )
        last_insert_id = result.lastrowid

        # data = result.fetchall()  # result.fetchall()
        if last_insert_id:
            return last_insert_id
        else:
            return False


    async def updateEvent(self, data):
        try:
            #self.DB.begin()

            sqlQuery = text(
                """
                UPDATE daily_events 
                SET `event_action_type` = :event_action_type,`is_missing_event` = :is_missing_event,`missing_event_information` = :missing_event_information,`status` = :status,`comments` = :comments,`event_end_date_time` = :event_end_date_time,`event_end_user_utc_date_time` = :event_end_user_utc_date_time,`event_end_ip` = :event_end_ip  WHERE id = :id
                """
            )
            result = self.DB.execute(sqlQuery,
                                     {
                                         "event_action_type": data['event_action_type'],
                                         "is_missing_event": data['is_missing_event'],
                                         "event_penalty_id": data['event_penalty_id'],
                                         "missing_event_information": data['missing_event_information'],
                                         "status": data['status'],
                                         "comments": data['comments'],
                                         "event_end_date_time": data['event_end_date_time'],
                                         "event_end_user_utc_date_time": data['event_end_user_utc_date_time'],
                                         "event_end_ip": data['event_end_ip'],
                                         "id": data['id']
                                     }
                                     )


            self.DB.commit()

            if result.rowcount > 0:
                return "success"
            else:
                return "failed"

        except IntegrityError as e:
            #self.DB.rollback()
            return "failed"
        except Exception as e:
            #self.DB.rollback()
            #print(f"Error: {e}")
            return "error"

        finally:
            self.DB.close()

    async def isDepartureDone(self, user_id, user_utc_current_date):
        sqlQuery = text(
            """
            SELECT * 
            FROM daily_events 
            WHERE DATE(event_start_user_utc_date_time) = :event_start_user_utc_date 
            AND user_id = :user_id 
            AND event_name_id = :event_name_id
            ORDER BY id ASC 
            LIMIT 1
            """
        )

        event_start_user_utc_date = await self.Event.getDateFromUserUTCDate(user_utc_current_date)

        result = self.DB.execute(sqlQuery, {
            "user_id": user_id,
            "event_start_user_utc_date": event_start_user_utc_date,
            "event_name_id": await self.Event.getDepartureEventId()
        })

        resultData = result.fetchone()
        if resultData is not None and len(resultData) > 0:
            return self.JSON.getEncodeData(resultData)
        else:
            return False

    async def isLunchBreakDone(self, user_id, user_utc_current_date):
        sqlQuery = text(
            """
            SELECT * 
            FROM daily_events 
            WHERE DATE(event_start_user_utc_date_time) = :event_start_user_utc_date 
            AND user_id = :user_id 
            AND event_name_id = :event_name_id 
            ORDER BY id ASC 
            LIMIT 1
            """
        )

        event_start_user_utc_date = await self.Event.getDateFromUserUTCDate(user_utc_current_date)

        result = self.DB.execute(sqlQuery, {
            "user_id": user_id,
            "event_start_user_utc_date": event_start_user_utc_date,
            "event_name_id": await self.Event.getLunchBreakEventId()
        })

        resultData = result.fetchone()
        if resultData is not None and len(resultData) > 0:
            return self.JSON.getEncodeData(resultData)
        else:
            return False

    async def isArrivalDone(self, user_id, event_start_user_utc_date_time):
        sqlQuery = text(
            """
            SELECT * 
            FROM daily_events 
            WHERE DATE(event_start_user_utc_date_time) = :event_start_user_utc_date_time
            AND user_id = :user_id
            AND event_name_id = :event_name_id
            LIMIT 1
            """
        )

        event_start_user_utc_date = await self.Event.getDateFromUserUTCDate(event_start_user_utc_date_time)

        result = self.DB.execute(sqlQuery, {
            "user_id": user_id,
            "event_start_user_utc_date_time": event_start_user_utc_date,
            "event_name_id": await self.Event.getArrivalEventId()
        })

        resultData = result.fetchone()
        if resultData is not None and len(resultData) > 0:
            return self.JSON.getEncodeData(resultData)
        else:
            return False

    async def isDayClosed(self, user_id, user_utc_current_date):
        sqlQuery = text(
            """
            SELECT * 
            FROM daily_events 
            WHERE DATE(event_start_user_utc_date_time) = :event_start_user_utc_date_time
            AND user_id = :user_id
            AND ((event_name_id = :arrival_id and  status = 2) or (event_name_id = :departure_id and  status = 1) )
            LIMIT 1
            """
        )

        event_start_user_utc_date = await self.Event.getDateFromUserUTCDate(user_utc_current_date)

        result = self.DB.execute(sqlQuery, {
            "user_id": user_id,
            "event_start_user_utc_date_time": event_start_user_utc_date,
            "arrival_id": await self.Event.getArrivalEventId(),
            "departure_id": await self.Event.getDepartureEventId()
        })

        resultData = result.fetchone()
        if resultData is not None and len(resultData) > 0:
            return self.JSON.getEncodeData(resultData)
        else:
            return False

    async def isMissingEventDone(self, user_id, user_utc_current_date):
        sqlQuery = text(
            """
            SELECT * 
            FROM daily_events 
            WHERE DATE(event_start_user_utc_date_time) = :event_start_user_utc_date_time
            AND user_id = :user_id
            AND is_missing_event=:is_missing_event
            order by id desc LIMIT 1
            """
        )

        event_start_user_utc_date = await self.Event.getDateFromUserUTCDate(user_utc_current_date)

        result = self.DB.execute(sqlQuery, {
            "user_id": user_id,
            "event_start_user_utc_date_time": event_start_user_utc_date,
            "is_missing_event":1
        })

        resultData = result.fetchone()
        if resultData is not None and len(resultData) > 0:
            return self.JSON.getEncodeData(resultData)
        else:
            return False

    async def getLastArrivalEvent(self, user_id):
        sqlQuery = text(
            """
            SELECT * 
            FROM daily_events 
            WHERE user_id=:user_id AND event_name_id=:event_name_id AND status =:status
            LIMIT 1
            """
        )

        result = self.DB.execute(sqlQuery, {
            "user_id": user_id,
            "event_name_id": await self.Event.getArrivalEventId(),
            "status":1
        })


        resultData = result.fetchone()
        if resultData is not None and len(resultData) > 0:
            return self.JSON.getEncodeData(resultData)
        else:
            return False




    async def getLastActiveEvent(self, user_id):
        sqlQuery = text(
            """
            SELECT * 
            FROM daily_events 
            WHERE user_id=:user_id AND status=:status
            order by id desc limit 1 
            """
        )

        result = self.DB.execute(sqlQuery, {
            "user_id": user_id,
            "status": 1
        })


        resultData = result.fetchone()
        if resultData is not None and len(resultData) > 0:
            return self.JSON.getEncodeData(resultData)
        else:
            return False

    async def isRequestedEventExist(self, user_id,event_name_id,status, event_start_user_utc_date_time):
        sqlQuery = text(
            """
            SELECT * 
            FROM daily_events 
            WHERE DATE(event_start_user_utc_date_time) = :event_start_user_utc_date_time
            AND user_id = :user_id
            AND event_name_id = :event_name_id
             AND status = :status
            LIMIT 1
            """
        )

        event_start_user_utc_date = await self.Event.getDateFromUserUTCDate(event_start_user_utc_date_time)

        result = self.DB.execute(sqlQuery, {
            "event_start_user_utc_date_time": event_start_user_utc_date,
            "user_id": user_id,
            "event_name_id": event_name_id,
            "status": status
        })

        resultData = result.fetchone()
        if resultData is not None and len(resultData) > 0:
            return self.JSON.getEncodeData(resultData)
        else:
            return False

    async def isAnyEventActiveExceptAD(self, user_id,event_start_user_utc_date_time):
        sqlQuery = text(
            """
            SELECT * 
            FROM daily_events 
            WHERE DATE(event_start_user_utc_date_time) = :event_start_user_utc_date_time
            AND user_id = :user_id 
            AND status = :status
            AND event_name_id!=:departure_id
            AND event_name_id!=:arrival_id
            LIMIT 1
            """
        )

        event_start_user_utc_date = await self.Event.getDateFromUserUTCDate(event_start_user_utc_date_time)

        result = self.DB.execute(sqlQuery, {
            "event_start_user_utc_date_time": event_start_user_utc_date,
            "user_id": user_id,
            "status": 1,
            "departure_id": await self.Event.getDepartureEventId(),
            "arrival_id": await self.Event.getArrivalEventId()
        })

        resultData = result.fetchone()
        if resultData is not None and len(resultData) > 0:
            return self.JSON.getEncodeData(resultData)
        else:
            return False





    async def getCurrentEventList(self, user_id,user_utc_current_date):

        sqlQuery = text(
            """
            SELECT * 
                FROM daily_events 
                WHERE (DATE(event_start_user_utc_date_time) = :event_start_user_utc_date) 
                AND user_id = :user_id order by id ASC 
            """
        )


        event_start_user_utc_date = await self.Event.getDateFromUserUTCDate(user_utc_current_date)

        result =  self.DB.execute(sqlQuery, {
            "user_id": user_id,
            "event_start_user_utc_date": event_start_user_utc_date,
        })

        resultData = result.fetchall()
        # return await self.Event.getEventList(currentEventId=False, status=1, dataList=False)
        if len(resultData) <= 0:
            return await self.Event.getEventList()

        elif resultData == "":
            return await self.Event.getEventList()
        else:
            data= await self.fetchData(result, resultData)

            if len(resultData)>1:
                del data[0]

                eventKeyList={
                    "arrival":False,
                    "lunch_break": False,
                    "teen_minutes": False,
                    "away": False,
                    "task_out": False,
                    "departure": False
                }
                lastEventId=1
                lastEventStatus = 1
                toDayDepartureDone=False

                for item in data:
                    eventKeyName=await self.Event.getExtractedEventKey(item['event_name_id'])
                    eventKeyList[eventKeyName]=True
                    lastEventId=item['event_name_id']
                    lastEventStatus = item['status']
                    isDepartureRequest=await self.Event.isDepartureRequest(lastEventId)
                    if isDepartureRequest:
                        toDayDepartureDone=True

                #print(eventKeyList)
                if toDayDepartureDone==False:
                    return await self.Event.getEventList(lastEventId,lastEventStatus,eventKeyList)
                else:
                    return {
                                0: "Today already departure",
                            }

            else:
                if data[0]['event_name_id']==1:
                    return await self.Event.getEventList(1)
                else:
                    # rear condition
                    return await self.Event.getEventList()



    async def showEventInformation(self, user_id, event_from_date, event_to_date):

        sqlQuery = text(
            """
                            SELECT 
                                DATE(event_start_user_utc_date_time) user_utc_action_date,
                                daily_events.*
                            FROM 
                                daily_events 
                            WHERE 
                                daily_events.user_id = :user_id 
                                AND DATE(daily_events.event_start_user_utc_date_time) >= :event_from_date 
                                AND DATE(daily_events.event_start_user_utc_date_time) <= :event_to_date
                            ORDER BY 
                                daily_events.id ASC
                     """
                        )

        # Assuming event_from_date and event_to_date are already datetime objects
        result = self.DB.execute(sqlQuery, {
            "user_id": user_id,
            "event_from_date": event_from_date,  # Ensure only date is considered
            "event_to_date": event_to_date,  # Ensure only date is considered
        })

        resultData = result.fetchall()

        # return await self.Event.getEventList(currentEventId=False, status=1, dataList=False)

        if len(resultData) <= 0:
            return False

        else:
            data= await self.fetchData(result, resultData)

            if len(resultData)>0:
                return await self.Event.customizeEventIfo(data)
            else:
                return False