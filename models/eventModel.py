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
            INSERT INTO daily_events (`user_id`,`event_name_id`,`status`,`comments`,`event_start_ip`, `event_start_user_utc_date_time`, `event_action_type`)
            VALUES (:user_id, :event_name_id, :status, :comments, :event_start_ip, :event_start_user_utc_date_time,:event_action_type)
            """
        )
        result = self.DB.execute(sqlQuery,
                                 {
                                      "user_id": data.user_id,
                                      "event_name_id":data.event_name_id,
                                       "status": self.Event.getStartStatus(),
                                      "comments": data.comments,
                                      "event_start_ip": data.user_ip,
                                     "event_start_user_utc_date_time":objectData['action_user_utc_date_time'],
                                     "event_action_type":objectData['event_action_type'],

                                 }
                                 )
        last_insert_id = result.lastrowid

        # data = result.fetchall()  # result.fetchall()
        if last_insert_id:
            return last_insert_id
        else:
            return False

    async def systemDeparture(self,data,objectData):

        sqlQuery = text(
            """
            INSERT INTO daily_events (`user_id`,`event_name_id`,`status`,`comments`,`event_start_ip`, `event_start_user_utc_date_time`, `event_action_type`, `auto_departure_user_utc_date_time`)
            VALUES (:user_id, :event_name_id, :status, :comments, :event_start_ip, :event_start_user_utc_date_time,:event_action_type,:auto_departure_user_utc_date_time)
            """
        )

        result = self.DB.execute(sqlQuery,
                                 {
                                      "user_id": objectData['user_id'],
                                      "event_name_id":self.Event.getDepartureID(),
                                      "status": self.Event.getStartStatus(),
                                      "comments":objectData['comments'],
                                     "event_start_user_utc_date_time":objectData['action_user_utc_date_time'],
                                     "event_action_type":objectData['event_action_type'],
                                     "event_start_ip": data.user_ip,
                                     "auto_departure_user_utc_date_time":objectData['auto_departure_user_utc_date_time']

                                 }
                                 )
        last_insert_id = result.lastrowid

        # data = result.fetchall()  # result.fetchall()
        if last_insert_id:
            return last_insert_id
        else:
            return False



    async def getLastArrivalEvent(self, user_id):
        sqlQuery = text(
            """
            SELECT * 
            FROM daily_events 
            WHERE user_id=:user_id AND event_name_id=:event_name_id
            order by id desc LIMIT 1
            """
        )

        result = self.DB.execute(sqlQuery, {
            "user_id": user_id,
            "event_name_id": self.Event.getArrivalID(),
        })


        resultData = result.fetchone()
        if resultData is not None and len(resultData) > 0:
            return self.JSON.getEncodeData(resultData)
        else:
            return False

    async def isDeparture(self, user_id, user_utc_current_date):
        sqlQuery = text(
            """
            SELECT * 
            FROM daily_events 
            WHERE (DATE(event_start_user_utc_date_time) = :event_start_user_utc_date) 
            AND user_id = :user_id 
            AND event_name_id = :event_name_id
            ORDER BY id ASC 
            LIMIT 1
            """
        )


        event_start_user_utc_date = await self.Event.getDateFromUserUTCDate(user_utc_current_date)
        #print(event_start_user_utc_date)
        result = self.DB.execute(sqlQuery, {
            "user_id": user_id,
            "event_start_user_utc_date": event_start_user_utc_date,
            "event_name_id": self.Event.getDepartureID()
        })

        resultData = result.fetchone()
        if resultData is not None and len(resultData) > 0:
            return True#self.JSON.getEncodeData(resultData)
        else:
            return False

    async def getAllEventDataByDate(self, user_id, user_utc_date):
        sqlQuery = text(
            """
            SELECT * 
            FROM daily_events 
            WHERE DATE(event_start_user_utc_date_time) = :event_start_user_utc_date_time
            AND user_id = :user_id
            """
        )

        event_user_utc_date = await self.Event.getDateFromUserUTCDate(user_utc_date)

        result = self.DB.execute(sqlQuery, {
            "user_id": user_id,
            "event_start_user_utc_date_time": event_user_utc_date,
        })

        resultData = result.fetchall()
        data = await self.fetchData(result, resultData)
        if resultData is not None and len(data) > 0:

            return data
        else:
            return False

    async def isExistEventByEventData(self,data,event_name_id):
        eventStatus=False
        for objectData in data:
            if objectData['event_name_id']==event_name_id:
                eventStatus=True
        return eventStatus

    async def getEventListObjectList(self,conditionEvent=False):
        if (conditionEvent):

            if conditionEvent=="dayClosed":
                return {
                      "0": "Today already departure",
                }
            else:

                return await self.Event.getCurrentEventListByData(conditionEvent)

        else:
            return {
                "1":"Arrival"
            }

    async def getDateWiseMonthData(self, user_id, user_date):

        sqlQuery = text(
            """
                            SELECT 
                                daily_events.*
                            FROM 
                                daily_events 
                            WHERE 
                                daily_events.user_id = :user_id 
                                AND (DATE(daily_events.event_start_user_utc_date_time) >= :event_from_date  AND DATE(daily_events.event_start_user_utc_date_time) <= :event_to_date )

                            ORDER BY 
                                daily_events.id ASC
                     """
        )

        start_date = await  self.Frz.getFirstDateOfMonthByDate(user_date)
        end_date = await  self.Frz.getLirstDateOfMonthByDate(user_date)

        # Assuming event_from_date and event_to_date are already datetime objects
        result = self.DB.execute(sqlQuery, {
            "user_id": user_id,
            "event_from_date": start_date,  # Ensure only date is considered
            "event_to_date": end_date,  # Ensure only date is considered
        })

        resultData = result.fetchall()

        if len(resultData) <= 0:
            return False
        else:
            data = await self.fetchData(result, resultData)

            if len(resultData) > 0:

                return data
            else:
                return False
    async def showEventInformation(self, user_id, event_from_date, event_to_date,utcDbData):


        sqlQuery = text(
            """
                            SELECT 
                                daily_events.*
                            FROM 
                                daily_events 
                            WHERE 
                                daily_events.user_id = :user_id 
                                AND (DATE(daily_events.event_start_user_utc_date_time) >= :event_from_date  AND DATE(daily_events.event_start_user_utc_date_time) <= :event_to_date )
                                
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


        if len(resultData) <= 0:
            return False
        else:
            data= await self.fetchData(result, resultData)

            if len(resultData)>0:
                user_utc_current_date = await self.Frz.getDateTimeByUTC(int(utcDbData['time_zone']), True)
                total_month_data =await  self.getDateWiseMonthData(user_id,user_utc_current_date)

                total_month_data= await self.Event.getEventInformationDetails(total_month_data,utcDbData)


                #print("================>")
                required_data= await self.Event.getEventInformationDetails(data, utcDbData)

                #print(total_month_data['total_actual_working_time'])
                return {
                    "current_month_spend_working_time": total_month_data['total_spend_working_time'],
                    "current_month_actual_working_time":total_month_data['total_actual_working_time'],
                    "current_month_actual_working_day": total_month_data['total_actual_working_day'],
                    "required_data": required_data,
                }

            else:
                return False