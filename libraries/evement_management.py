from datetime import datetime, timedelta
import random
import string

class EventManagement:
    def __init__(self):
        pass

    async def getEventData(self, eventId=False):
        eventDist = {
            1:{ "name":"Arrival", "min":0,"max":0,"required":False },
            2:{ "name":"Lunch break","min":30,"max":120,"required":True },
            3: {"name": "Departure", "min": 0, "max": 0, "required": False}, # it is single event no return
            4: {"name": "10 minutes walk", "min": 10, "max": 120, "required": False},
            5: {"name": "Away", "min": 0, "max": 0, "required": False},
            6: {"name": "Task outside office", "min": 0, "max": 1200, "required": False},

        }
        if eventId:
            return eventDist.get(eventId, "event ID not found")
        else:
            return eventDist

    async def getExtractedEventKey(self,eventId):
            if eventId==1:
                return "arrival"
            elif eventId==2:
                return "lunch_break"
            elif eventId == 4:
                return "teen_minutes"
            elif eventId == 5:
                return "away"
            elif eventId == 6:
                return "task_out"
            else:
                return "departure"

    async def getEventList(self, currentEventId=False, status=1, dataList=False):
        if currentEventId == False:
            return {
                1: "New Arrival",
            }
        elif currentEventId == 1:
            return {
                2: "Lunch break",
                4: "10 minutes walk",
                5: "Away",
                6: "Task outside office",
                3: "Departure",
            }
        elif currentEventId == 2 and status == 1:
            return {
                2: "Return from lunch break",
            }
        elif currentEventId == 4 and status == 1:
            return {
                4: "Return from 10 minutes walk",
            }
        elif currentEventId == 5 and status == 1:
            return {
                5: "Return Away",
            }
        elif currentEventId == 6 and status == 1:
            return {
                6: "Return task outside office",
            }
        else:
            if dataList:
                if dataList['lunch_break'] and dataList['teen_minutes'] and dataList['away'] and dataList['task_out']:
                    return {
                        3: "Departure",
                    }
                elif dataList['lunch_break'] and dataList['teen_minutes'] and dataList['away'] and not dataList[
                    'task_out']:
                    return {
                        6: "Task outside office",
                        3: "Departure",
                    }
                elif dataList['lunch_break'] and dataList['teen_minutes'] and not dataList['away'] and not dataList[
                    'task_out']:
                    return {
                        5: "Away",
                        6: "Task outside office",
                        3: "Departure",
                    }
                elif dataList['lunch_break'] and not dataList['teen_minutes'] and not dataList['away'] and not dataList[
                    'task_out']:
                    return {
                        4: "10 minutes walk",
                        5: "Away",
                        6: "Task outside office",
                        3: "Departure",
                    }
                else:
                    return {
                        2: "Lunch break",
                        4: "10 minutes walk",
                        5: "Away",
                        6: "Task outside office",
                        3: "Departure",
                    }
            else:
                return {
                    2: "Lunch break",
                    4: "10 minutes walk",
                    5: "Away",
                    6: "Task outside office",
                    3: "Departure",
                }


    async def getArrivalEventId(self):
        return 1
    async def getLunchBreakEventId(self):
        return 2

    async def getDepartureEventId(self):
        return 3
    async def isDepartureRequest(self, eventId):
        if eventId==3:
            return True
        else:
            return False
    async def isArrivalRequest(self, eventId):
        if eventId==1:
            return True
        else:
            return False
    async def eventStatusDayOver(self, eventId,extra_data=False):
        if eventId == 1:
            return {
                "event_action_type": 3,
                "is_missing_event":1,
                "event_penalty_id":1,
                "missing_event_information": "Missing Lunch break and Departure",
            }
        elif eventId == 2:
            return {
                "event_action_type": 3,
                "is_missing_event":1,
                "event_penalty_id":2,
                "missing_event_information": "Missing Lunch break return and Departure",
            }
        elif eventId ==4:
            if extra_data['lunch_break']==True:
                # user did lunch break properly
                return {
                    "event_action_type": 3,
                    "is_missing_event": 1,
                    "event_penalty_id": 3,
                    "missing_event_information": "Missing 10 minutes walk return and Departure",
                }
            else:
                # user did not lunch break properly
                return {
                    "event_action_type": 3,
                    "is_missing_event": 1,
                    "event_penalty_id": 4,
                    "missing_event_information": "Missing 10 minutes walk return and Lunch break and Departure",
                }
        elif eventId == 5:

            if extra_data['lunch_break'] == True:
                # user did lunch break properly
                return {
                    "event_action_type": 3,
                    "is_missing_event": 1,
                    "event_penalty_id": 5,
                    "missing_event_information": "Missing Away return and Departure",
                }
            else:
                # user did not lunch break properly
                return {
                    "event_action_type": 3,
                    "is_missing_event": 1,
                    "event_penalty_id": 6,
                    "missing_event_information": "Missing Away return and Lunch break and Departure",
                }
        elif eventId == 6:
            return {
                "event_action_type": 3,
                "is_missing_event": 1,
                "event_penalty_id": 7,
                "missing_event_information": "Missing Task outside office return",
            }
        else:
            return {
                "event_action_type": 3,
                "is_missing_event": 0,
                "event_penalty_id": 0,
                "missing_event_information": False,
            }

    async def eventStatusInnerDay(self, eventId, extra_data=False):
        if eventId == 3:
            # make departure event
            if extra_data['lunch_break'] == True:
                # user did lunch break properly
                return {
                    "event_action_type": 2,
                    "is_missing_event": 0,
                    "event_penalty_id":0,
                    "missing_event_information": "",
                }
            else:
                # user did not lunch break properly
                return {
                    "event_action_type": 2,
                    "is_missing_event": 1,
                    "event_penalty_id": 8,
                    "missing_event_information": "Missing Lunch break ",
                }


        else:
            return {
                "event_action_type": 2,
                "is_missing_event": 0,
                "event_penalty_id": 0,
                "missing_event_information": "",
            }

    async def isLunchBreakDone(self,statusCode):
        if statusCode=="success":
            return True
        else:
            return False
    async def getHoursByMinuts(self, minutes):
        hours = minutes / 60
        return hours
        minutes = 720
        hours = minutes_to_hours(minutes)
        return hours

    async def isTimeOver(self, user_UTC_current_time, user_UTC_action_event_time):
        # Define the date format
        date_format = "%Y-%m-%d %I:%M:%S %p"

        # Parse the datetime strings into datetime objects
        start_datetime = datetime.strptime(user_UTC_action_event_time, date_format)
        end_datetime = datetime.strptime(user_UTC_current_time, date_format)

        # Calculate the time difference
        time_difference = end_datetime - start_datetime

        # Convert the difference to total minutes
        total_minutes = time_difference.total_seconds() / 60

        return total_minutes

    async def isWorkTimeAvailable(self,from_date, to_date):
        # Extracting date strings from the dictionaries

        from_date_str = from_date
        to_date_str = to_date
        # Convert string dates to datetime objects
        from_date_dt = datetime.strptime(from_date_str, "%Y-%m-%d %I:%M:%S %p")
        to_date_dt = datetime.strptime(to_date_str, "%Y-%m-%d %I:%M:%S %p")

        # Calculate the duration between the dates
        duration = to_date_dt - from_date_dt

        # Check if the duration is more than or equal to 20 hours or if the dates are different
        if duration.total_seconds() / 3600 >= 20 or from_date_dt.date() != to_date_dt.date():
            return False # time is over
        else:
            return True

    async def isSameDate(self, from_date, to_date):
        # Convert strings to datetime objects
        from_date_dt =  datetime.strptime(from_date, "%Y-%m-%d %I:%M:%S %p")
        to_date_dt =  datetime.strptime(to_date, "%Y-%m-%d %I:%M:%S %p")

        # Extract date part from datetime objects
        from_date_date = from_date_dt.date()
        to_date_date = to_date_dt.date()

        # Check if the dates are the same
        return from_date_date == to_date_date

    async def isValidLoinSession(self, from_date, to_date):
        # Convert strings to datetime objects
        from_date_dt = datetime.strptime(from_date, "%Y-%m-%d %I:%M:%S %p")
        to_date_dt = datetime.strptime(to_date, "%Y-%m-%d %I:%M:%S %p")

        # Extract date part from datetime objects
        from_date_date = from_date_dt.date()
        to_date_date = to_date_dt.date()

        # Check if the dates are the same
        return from_date_date == to_date_date

    async def getDateFromString(self, from_date):
        # Convert strings to datetime objects
        from_date_dt = datetime.strptime(from_date, "%Y-%m-%dT%H:%M:%S")

        # Extract date part from datetime objects
        return from_date_dt.date()
    async def getDateFromUserUTCDate(self, from_date):
        # Convert strings to datetime objects
        datetime_obj = datetime.strptime(from_date, "%Y-%m-%d %I:%M:%S %p")
        # Extract date part from datetime objects
        return datetime_obj.date()

    async def eventStatusText(self,id):
        data= {
            1: "Active",
            2: "Done",
            3: "Reject",
            4: "Error",
        }
        return data.get(id, data[4])

    async def getEvenObjectInfo(self, objectData,event_name,comments):
        if len(objectData)>0:

            event_date_time=objectData['event_start_user_utc_date_time']
            if objectData['status']==2:
                event_date_time = objectData['event_end_user_utc_date_time']

            datetime_obj = ""#datetime.strptime(event_date_time, "%Y-%m-%d %I:%M:%S %p")
            short_date ="" #datetime_obj.date()
            short_time =  ""#datetime_obj.strftime("%I:%M:%S %p")

            return {
                "db_id": objectData['id'],
                "db_date_time":objectData['created_at'],
                "event_name_id": objectData['event_name_id'],
                "name": event_name,
                "date": short_date,
                "time": short_time,
                "comments": comments,
                "is_missing_event": objectData['is_missing_event'],
                "missing_event_information": objectData['missing_event_information'],
                "status_code": objectData['status'],
                "status": await self.eventStatusText(objectData['status']),
                "user_ip": objectData['event_start_ip']
            }

        else:
            return {
                "db_id":"0",
                "db_date_time": "",
                "event_name_id":"",
                "name": event_name,
                "date": "",
                "time": "",
                "comments": comments,
                "is_missing_event": "",
                "missing_event_information": "",
                "status_code": "",
                "status": "N/A",
                "user_ip": "N/A"
            }
    async def customizeEventIfo(self,data):

        object_data = {}
        for item in data:

            arrival = await self.getEvenObjectInfo("", "Arrival", "No Information found")
            departure = await self.getEvenObjectInfo("", "Departure", "Missing event")
            lunch_break =  await self.getEvenObjectInfo("", "Lunch break", "Missing event")

            lunch_break_return =  await self.getEvenObjectInfo("", "Return from lunch break", "Missing event")
            ten_minutes_return = await self.getEvenObjectInfo("", "Return from 10 minutes walk", "Missing event")
            away_return =  await self.getEvenObjectInfo("", "Return from away", "Missing event")
            task_out_side_return =  await self.getEvenObjectInfo(item, "Return from task outside", "Missing event")


            ten_minutes = await self.getEvenObjectInfo("", "10 minutes walk", "")
            away = await self.getEvenObjectInfo("", "Away", "")
            task_out_side = await self.getEvenObjectInfo("", "Task outside office", "")




            if item['event_name_id']==1:
                comments=""
                arrival= await self.getEvenObjectInfo(item,"Arrival",comments)

            if item['event_name_id'] == 2:
                comments = ""
                lunch_break = await self.getEvenObjectInfo(item, "Lunch break", comments)

            if item['event_name_id'] == 4:
                comments = ""
                ten_minutes = await self.getEvenObjectInfo(item, "10 minutes walk", comments)

            if item['event_name_id'] == 5:
                comments = ""
                away = await self.getEvenObjectInfo(item, "Away", comments)

            if item['event_name_id'] == 6:
                comments = ""
                task_out_side = await self.getEvenObjectInfo(item, "Task outside office", comments)

            if item['event_name_id'] == 2 and item['status']==2:
                comments = ""
                lunch_break_return = await self.getEvenObjectInfo(item, "Return from lunch break", comments)

            if item['event_name_id'] == 4 and item['status'] == 2:
                comments = ""
                ten_minutes_return = await self.getEvenObjectInfo(item, "Return from 10 minutes walk", comments)

            if item['event_name_id'] == 5 and item['status'] == 2:
                comments = ""
                away_return = await self.getEvenObjectInfo(item, "Return from away", comments)

            if item['event_name_id'] == 6 and item['status'] == 2:
                comments = ""
                task_out_side_return = await self.getEvenObjectInfo(item, "Return from task outside", comments)

            if item['event_name_id'] == 3:
                comments = ""
                departure = await self.getEvenObjectInfo(item, "Departure", comments)

            if item['user_utc_action_date'] in object_data:
                key_data = object_data[item['user_utc_action_date']]
            else:
                key_data = []


            if lunch_break['event_name_id'] == 2:
                if lunch_break['status_code'] == 2 or (lunch_break['status_code'] == 1 and departure['event_name_id'] == 3):
                    key_data.append([lunch_break, lunch_break_return])
                else:
                    key_data.append([lunch_break])

            if ten_minutes['event_name_id'] == 4:
                if ten_minutes['status_code'] == 2 or (ten_minutes['status_code'] == 1 and departure['event_name_id'] == 3):
                    key_data.append([ten_minutes, ten_minutes_return])
                else:
                    key_data.append([ten_minutes])

            if away['event_name_id'] == 5:
                if away['status_code'] == 2 or (away['status_code'] == 1 and departure['event_name_id'] == 3):
                    key_data.append([away, away_return])
                else:
                    key_data.append([away])

            if task_out_side['event_name_id'] == 6:
                if task_out_side['status_code'] == 2 or (task_out_side['status_code'] == 1 and departure['event_name_id'] == 3):
                    key_data.append([task_out_side, task_out_side_return])
                else:
                    key_data.append([task_out_side])

            object_data[item['user_utc_action_date']] = key_data if key_data else [[arrival]]

        return object_data


