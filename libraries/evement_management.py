from datetime import datetime, timedelta
import random
import string
from pprint import pprint
import re

from libraries.frz import  Frz

from libraries.jsonFormate import JsonFormate
class EventManagement:
    def __init__(self):
        self.JSON = JsonFormate()
        self.Frz = Frz()

    def getEventNameByID(self, eventID):
        data = {
            "1": "Arrival",
            "2": "Departure",
            "3": "Lunch break",
            "4": "Return lunch break",
            "5": "10 minutes walk",
            "6": "Return 10 minutes walk",
            "7": "Away",
            "8": "Return away ",
            "9": "Task outside office",
            "10": "Return task outside office",
        }


        # Using get method
        event_name = data.get(str(eventID))
        if event_name:
            return event_name
        else:
            return False #f"No event found with ID {eventID}"
    def getRequiredMaximumMinutes(self,eventId):
        eight_hours_minutes=8*60
        data = {
            "2": 120,
            "3": 120,
            "5": eight_hours_minutes,
            "7": eight_hours_minutes,
            "9": 0,
            "0":240 # special_lunch_departure
        }
        required_minuties = data.get(str(eventId))
        if required_minuties:
            return required_minuties
        else:
            return 0
    def getRequiredMinimumMinutes(self,eventId):
        data = {
            "3": 30,
            "5": 0,
            "7": 0,
            "9": 0,
        }
        required_minuties = data.get(str(eventId))
        if required_minuties:
            return required_minuties
        else:
            return 0
    def getStartStatus(self):
        return 1
    def getAutoDepartureStatus(self):
        return 2
    def getArrivalID(self):
        return 1
    def getDepartureID(self):
        return 2
    def getLunchBreakID(self):
        return 3

    def getLunchBreakReturnID(self):
        return 4
    def getTenMinitID(self):
        return 5

    def getTenMinitReturnID(self):
        return 6

    def getAwayID(self):
        return 7

    def getAwayReturnID(self):
        return 8

    def getTaskOutsideID(self):
        return 9

    def getTaskOutsideReturnID(self):
        return 10

    def isArrivalRequest(self, eventId):
        if eventId == 1:
            return True
        else:
            return False
    def isDepartureRequest(self, eventId):
        if eventId==2:
            return True
        else:
            return False

    def isLunchBreakRequest(self, eventId):
        if eventId == 3:
            return True
        else:
            return False

    def isLunchBreakReturnRequest(self, eventId):
        if eventId == 4:
            return True
        else:
            return False

    def isTenMinutesRequest(self, eventId):
        if eventId == 5:
            return True
        else:
            return False

    def isTenMinutesReturnRequest(self, eventId):
        if eventId == 6:
            return True
        else:
            return False

    def isAwayRequest(self, eventId):
        if eventId == 7:
            return True
        else:
            return False

    def isAwayReturnRequest(self, eventId):
        if eventId == 8:
            return True
        else:
            return False

    def isTaskOutSideRequest(self, eventId):
        if eventId == 9:
            return True
        else:
            return False

    def isTaskOutSideReturnRequest(self, eventId):
        if eventId == 10:
            return True
        else:
            return False


    async def getDayNameFromDate(self,date_str):
        date_object = datetime.strptime(date_str, '%Y-%m-%d')
        day_name = date_object.strftime('%A')
        return day_name

    async def getMonthNameFromDate(self,date_str):
        date_object = datetime.strptime(date_str, '%Y-%m-%d')
        month_name = date_object.strftime('%B')
        return month_name

    async def getYearNameFromDate(self, date_str):
        date_object = datetime.strptime(date_str, '%Y-%m-%d')
        year_full = date_object.strftime('%Y')
        return year_full

    async def isValidRequest(self,event_data,event_name_id):
        source_data=[]
        for objectData in event_data:
            source_data.append(objectData['event_name_id'])


        if event_name_id in source_data:
            return False
        elif self.isLunchBreakRequest(event_name_id):

            if (self.getArrivalID() not in source_data):
                return False
            elif (self.getLunchBreakReturnID() in source_data):
                return False
            elif (self.getTenMinitID() in source_data and self.getTenMinitReturnID() not in source_data):
                return False
            elif (self.getAwayID() in source_data and self.getAwayReturnID() not in source_data):
                return False
            elif (self.getTaskOutsideID() in source_data and self.getTaskOutsideReturnID() not in source_data):
                return False
            else:
                return True
        elif self.isLunchBreakReturnRequest(event_name_id):
            if (self.getLunchBreakID() not in source_data):
                return False
            else:
                return True
        elif self.isTenMinutesRequest(event_name_id):

            if (self.getTenMinitReturnID() in source_data):
                return False
            elif (self.getArrivalID() not in source_data):
                return False
            elif (self.getAwayID() in source_data and self.getAwayReturnID() not in source_data):
                return False
            elif (self.getTaskOutsideID() in source_data and self.getTaskOutsideReturnID() not in source_data):
                return False
            else:
                return True
        elif self.isTenMinutesReturnRequest(event_name_id):
            if (self.getTenMinitID() not in source_data):
                return False
            else:
                return True
        elif self.isAwayRequest(event_name_id):

            if (self.getAwayReturnID() in source_data):
                return False
            elif (self.getArrivalID() not in source_data):
                return False
            elif (self.getTenMinitID() in source_data and self.getTenMinitReturnID() not in source_data):
                return False
            elif (self.getTaskOutsideID() in source_data and self.getTaskOutsideReturnID() not in source_data):
                return False
            else:
                return True
        elif self.isAwayReturnRequest(event_name_id):
            if (self.getAwayID() not in source_data):
                return False
            else:
                return True

        elif self.isTaskOutSideRequest(event_name_id):

            if (self.getTaskOutsideReturnID() in source_data):
                return False
            elif (self.getArrivalID() not in source_data):
                return False
            elif (self.getTenMinitID() in source_data and self.getTenMinitReturnID() not in source_data):
                return False
            elif (self.getAwayID() in source_data and self.getAwayReturnID() not in source_data):
                return False
            else:
                return True

        elif self.isTaskOutSideReturnRequest(event_name_id):
            if (self.getTaskOutsideID() not in source_data):
                return False
            else:
                return True

        elif self.isDepartureRequest(event_name_id):
            if (self.getTenMinitID() in source_data and self.getTenMinitReturnID() not in source_data):
                return False
            elif (self.getAwayID() in source_data and self.getAwayReturnID() not in source_data):
                return False
            elif (self.getTaskOutsideID() in source_data and self.getTaskOutsideReturnID() not in source_data):
                return False
            elif (self.getLunchBreakID() in source_data and self.getLunchBreakReturnID() not in source_data):
                return False
            else:
                return True


    async def getCurrentEventListByData(self,event_data):
        source_data=[]
        for objectData in event_data:
            source_data.append(objectData['event_name_id'])

        #print(source_data)


        if (self.getArrivalID() in source_data and self.getDepartureID() in source_data):
            return {
                "0": "Today already departure",
            }
        elif (self.getLunchBreakID() in source_data and (self.getLunchBreakReturnID() not in source_data)):
            return {
                "4": "Return lunch break ",
            }
        elif (self.getTenMinitID() in source_data and (self.getTenMinitReturnID() not in source_data)):
            return {
                "6": "Return 10 minutes walk ",
            }

        elif (self.getAwayID() in source_data and (self.getAwayReturnID() not in source_data)):
            return {
                "8": "Return away ",
            }
        elif (self.getTaskOutsideID() in source_data and (self.getTaskOutsideReturnID() not in source_data)):
            return {
                "10": "Return task outside office ",
            }

        elif (self.getArrivalID() in source_data and (self.getLunchBreakID() not in source_data and self.getTenMinitID() not in source_data and self.getAwayID() not in source_data and self.getTaskOutsideID() not in source_data)):
            return {
                "3": "Lunch break",
                "5": "10 minutes walk",
                "7": "Away",
                "9": "Task outside office",
                "2": "Departure",
            }


        elif (self.getArrivalID() in source_data and (
                self.getLunchBreakID() not in source_data and self.getTenMinitID() not in source_data and self.getAwayID() not in source_data and self.getTaskOutsideReturnID()  in source_data)):
            return {
                "3": "Lunch break",
                "5": "10 minutes walk",
                "7": "Away",
                "2": "Departure",
            }

        elif (self.getArrivalID() in source_data and (
                self.getLunchBreakID() not in source_data and self.getTenMinitID() not in source_data and self.getAwayReturnID() in source_data and self.getTaskOutsideID() not in source_data)):
            return {
                "3": "Lunch break",
                "5": "10 minutes walk",
                "9": "Task outside office",
                "2": "Departure",
            }

        elif (self.getArrivalID() in source_data and (self.getLunchBreakID() not in source_data and self.getTenMinitID() not in source_data and self.getAwayReturnID() in source_data and self.getTaskOutsideReturnID() in source_data)):
            return {
                "3": "Lunch break",
                "5": "10 minutes walk",
                "2": "Departure",
            }

        elif (self.getArrivalID() in source_data and (self.getLunchBreakID() not in source_data and self.getTenMinitReturnID() in source_data and self.getAwayID() not in source_data and self.getTaskOutsideID() not in source_data)):
            return {
                "3": "Lunch break",
                "7": "Away",
                "9": "Task outside office",
                "2": "Departure",
            }
        elif (self.getArrivalID() in source_data and (
                self.getLunchBreakID() not in source_data and self.getTenMinitReturnID() in source_data and self.getAwayID() not in source_data and self.getTaskOutsideReturnID() in source_data)):
            return {
                "3": "Lunch break",
                "7": "Away",
                "2": "Departure",
            }
        elif (self.getArrivalID() in source_data and (
                self.getLunchBreakID() not in source_data and self.getTenMinitReturnID()  in source_data and self.getAwayReturnID() in source_data and self.getTaskOutsideID() not in source_data)):
            return {
                "3": "Lunch break",
                "9": "Task outside office",
                "2": "Departure",
            }
        elif (self.getArrivalID() in source_data and (
                self.getLunchBreakID() not in source_data and self.getTenMinitReturnID()  in source_data and self.getAwayReturnID()  in source_data and self.getTaskOutsideReturnID() in source_data)):
            return {
                "3": "Lunch break",
                "2": "Departure",
            }
        elif (self.getArrivalID() in source_data and (
                self.getLunchBreakReturnID() in source_data and self.getTenMinitID() not in source_data and self.getAwayID() not in source_data and self.getTaskOutsideID() not in source_data)):
            return {
                "5": "10 minutes walk",
                "7": "Away",
                "9": "Task outside office",
                "2": "Departure",
            }
        elif (self.getArrivalID() in source_data and (
                self.getLunchBreakReturnID() in source_data and self.getTenMinitID() not in source_data and self.getAwayID() not in source_data and self.getTaskOutsideReturnID()  in source_data)):
            return {
                "5": "10 minutes walk",
                "7": "Away",
                "2": "Departure",
            }
        elif (self.getArrivalID() in source_data and (
                self.getLunchBreakReturnID() in source_data and self.getTenMinitID() not in source_data and self.getAwayReturnID() in source_data and self.getTaskOutsideID() not in source_data)):
            return {
                "5": "10 minutes walk",
                "9": "Task outside office",
                "2": "Departure",
            }
        elif (self.getArrivalID() in source_data and (
                self.getLunchBreakReturnID() in source_data and self.getTenMinitID() not in source_data and self.getAwayReturnID() in source_data and self.getTaskOutsideReturnID() in source_data)):
            return {
                "5": "10 minutes walk",
                "2": "Departure",
            }
        elif (self.getArrivalID() in source_data and (
                self.getLunchBreakReturnID() in source_data and self.getTenMinitReturnID()  in source_data and self.getAwayID() not in source_data and self.getTaskOutsideID() not in source_data)):
            return {
                "7": "Away",
                "9": "Task outside office",
                "2": "Departure",
            }
        elif (self.getArrivalID() in source_data and (
                self.getLunchBreakReturnID() in source_data and self.getTenMinitReturnID()  in source_data and self.getAwayID() not in source_data and self.getTaskOutsideReturnID() in source_data)):
            return {
                "7": "Away",
                "2": "Departure",
            }
        elif (self.getArrivalID() in source_data and (
                self.getLunchBreakReturnID() in source_data and self.getTenMinitReturnID() in source_data and self.getAwayReturnID() in source_data and self.getTaskOutsideID() not in source_data)):
            return {
                "9": "Task outside office",
                "2": "Departure",
            }
        elif (self.getArrivalID() in source_data and (
                self.getLunchBreakReturnID() in source_data and self.getTenMinitReturnID()  in source_data and self.getAwayReturnID()  in source_data and self.getTaskOutsideReturnID()  in source_data)):
            return {
                "2": "Departure",
            }
        else:
            return {
                "0": "No event available",
            }

    async def getHoursByMinuts(self, minutes):
        hours = minutes / 60
        return hours
        minutes = 720
        hours = minutes_to_hours(minutes)
        return hours


    async def getMaxEightHours(self,request_date):
        from_date_datetime = datetime.strptime(request_date, "%Y-%m-%d %I:%M:%S %p")
        to_date_datetime = from_date_datetime + timedelta(hours=8)
        to_date = to_date_datetime.strftime("%Y-%m-%d %I:%M:%S %p")
        isSameDate=await self.isSameDate(request_date,to_date)
        if isSameDate:
            return to_date
        else:
            dateData=await self.getDateFromDate(request_date)
            return dateData+" 11:59:59 PM"
    async def getMaximumHoursDateTime(self,request_date):
        dateData=await self.getDateFromDate(request_date)
        return dateData+" 11:59:59 PM"
    async def getMinimumHoursDateTime(self,request_date):
        dateData=await self.getDateFromDate(request_date)
        return dateData+" 12:00:00 AM"

    async def isWorkTimeAvailable(self,from_date, to_date):
        # Extracting date strings from the dictionaries

        from_date_str = from_date
        to_date_str = to_date
        # Convert string dates to datetime objects
        from_date_dt = datetime.strptime(from_date_str, "%Y-%m-%d %I:%M:%S %p")
        to_date_dt = datetime.strptime(to_date_str, "%Y-%m-%d %I:%M:%S %p")

        # Calculate the duration between the dates
        duration = to_date_dt - from_date_dt

        # Check if the duration is more than or equal to 24 hours or if the dates are different
        if duration.total_seconds() / 3600 >= 24 or from_date_dt.date() != to_date_dt.date():
            return False # time is over
        else:
            return True
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
    async def isSameDate(self, from_date, to_date):
        # Convert strings to datetime objects

        #from_date_dt = datetime.strptime(from_date, "%Y-%m-%d %I:%M:%S %p")

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

    async def getTimeFromDatetime(self, date_string):
        date_dt = datetime.strptime(date_string, "%Y-%m-%d %I:%M:%S %p")

        return date_dt.strftime("%I:%M:%S %p")


    async def getDateFromDate(self, date_string):

        date_dt =datetime.strptime(date_string, "%Y-%m-%d %I:%M:%S %p")

        if isinstance(date_string, str):
            return  date_dt.strftime("%Y-%m-%d")
        else:
            return date_dt.date()



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

    async def getDifferTime(self, start_time_str, end_time_str, fullDateTime=False):
        # Convert strings to datetime objects
        start_time = datetime.strptime(start_time_str, "%I:%M:%S %p")
        end_time = datetime.strptime(end_time_str, "%I:%M:%S %p")

        # Check if start time is later or earlier than end time
        timeStatus = "Late" if start_time > end_time else "Early"

        # Calculate the difference
        time_diff = end_time - start_time

        # Extract hours and minutes from the difference
        hours = time_diff.seconds // 3600
        minutes = (time_diff.seconds % 3600) // 60

        if ((hours > 0 and minutes > 0) or (hours > 0 and minutes == 0) or (hours == 0 and minutes > 0)):

            hoursText = f"{hours} hours" if hours > 1 else f"{hours} hour and"
            minutesText = f"{minutes} minutes" if minutes > 1 else f"{minutes} minute"
            if fullDateTime:
                if hours >= 1:
                    return timeStatus + " " + hoursText + " " + minutesText
                else:
                    return timeStatus + " " + minutesText

            else:
                if hours >= 1:
                    return hoursText + " " + minutesText
                else:
                    return timeStatus + " " + minutesText

        else:
            if fullDateTime:
                return fullDateTime
            else:
                return False

    from datetime import datetime

    async def getStatusEarlYLate(self, action_time_str, default_time_str, isTimeCalculate=False):
        try:
            action_time = datetime.strptime(action_time_str, "%Y-%m-%d %I:%M:%S %p")
            default_time = datetime.strptime(default_time_str, "%Y-%m-%d %I:%M:%S %p")

            # Calculate the time difference
            time_diff = abs(default_time - action_time)

            # Extract hours, minutes, and seconds from the difference
            hours, remainder = divmod(time_diff.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            # Determine if the action time is early or late
            if action_time < default_time:
                status = "early"
            elif action_time > default_time:
                status = "late"
            else:
                status = "on time"

            # Construct the response message
            if status != "on time":
                if isTimeCalculate:
                    if status == "early":
                        if hours < 8 or (hours == 8 and minutes < 30):
                            response = f"{abs(hours)} hour{'s' if abs(hours) != 1 else ''} "
                            response += f"{minutes} minute{'s' if minutes != 1 else ''} "
                            response += f"{seconds} second{'s' if seconds != 1 else ''} {status}"
                        else:
                            response = action_time_str
                    else:
                        response = action_time_str
                else:
                    response = f"{abs(hours)} hour{'s' if abs(hours) != 1 else ''} "
                    response += f"{minutes} minute{'s' if minutes != 1 else ''} "
                    response += f"{seconds} second{'s' if seconds != 1 else ''} {status}"
            else:
                response = action_time_str

            return response
        except ValueError:
            return ""

    async def getGeneralFormatByMinutes(self, total_minutes):

        # Convert to seconds and split into integer and decimal parts
        total_seconds = total_minutes * 60
        minutes_from_seconds, seconds = divmod(total_seconds, 60)

        # Calculate hours and remaining minutes
        hours, remaining_minutes = divmod(total_minutes, 60)

        if hours > 0:
            if remaining_minutes > 0:
                return f"{round(hours)} hours, {round(remaining_minutes)} minutes, {round(seconds)} seconds"
            else:
                return f"{round(hours)} hours, {round(seconds)} seconds"
        elif remaining_minutes > 0:
            return f"{round(remaining_minutes)} minutes, {round(seconds)} seconds"
        else:
            return f"{round(seconds)} seconds"

    async def isValidDateTime(self, datetime_str):
        if datetime_str is None or datetime_str == "null" or datetime_str == " " or datetime_str == "00:00:00.000000":
            return False
        try:
            datetime.strptime(datetime_str, "%Y-%m-%d %I:%M:%S %p")
            return True
        except ValueError:
            return False

    async def getTimeStamp(self,fullDate):
        date_object = datetime.strptime(fullDate, "%Y-%m-%d")
        timestamp = date_object.timestamp()
        return timestamp

    async def getExistedEventDateTime(self, event_Data, event_name_id_to_check):
        for item in event_Data:
            if item['event_name_id'] == event_name_id_to_check:
                return item['event_action_user_utc_date_time']
        return False

    async def getExistedEventDateShortTime(self, event_Data, event_name_id_to_check):
        for item in event_Data:
            if item['event_name_id'] == event_name_id_to_check:
                return item['user_utc_time']
        return False

    async def getExistedEventAutoDepartureID(self, event_Data, event_name_id_to_check):

        for item in event_Data:
            if item['event_name_id'] == event_name_id_to_check and item['event_action_type']==self.getAutoDepartureStatus():
                return True
        return False

    async def getAutoDepartureComments(self, event_Data, event_name_id_to_check):
        for item in event_Data:
            if item['event_name_id'] == event_name_id_to_check:
                return item['comments']
        return False
    async def check_work_end(self,current_user_UTC_date_time_str, default_work_end_date_time_str):
        # Convert string to datetime objects
        current_user_UTC_date_time = datetime.strptime(current_user_UTC_date_time_str, "%Y-%m-%d %I:%M:%S %p")
        default_work_end_date_time = datetime.strptime(default_work_end_date_time_str, "%Y-%m-%d %I:%M:%S %p")

        # Check if current time is greater than or equal to default work end time
        if current_user_UTC_date_time >= default_work_end_date_time:
            return False
        else:
            return True

    async def get_index_of_event_data(self, data, event_name_id):
        if not data:
            return 0  # Return 0 if data is empty
        index_to_insert = len(data)  # Initialize to the length of data
        for i, obj in enumerate(data):
            if obj.get("event_name_id") == event_name_id:
                index_to_insert = i + 1  # Increment by 1 to insert after the found index
                break
        return index_to_insert

    async def contains_auto_departure_date(self,data):
        if data is None or not isinstance(data, str) or not data.strip():
            return False

        pattern = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} [AP]M"  # Regex pattern to match date strings
        return bool(re.search(pattern, data))
    async def getEventInformationDetails(self,main_data,userUTCData,requestType=False):

        eventData=main_data
        user_id = userUTCData['user_id']
        weekend_id = userUTCData['weekend_id']
        time_zone = userUTCData['time_zone']
        default_work_start_time = userUTCData['work_start_time']
        default_work_end_time = userUTCData['work_end_time']



        source_data = {}


        for item in eventData:

            missing_event=False
            event_action_user_utc_date_time = item['event_start_user_utc_date_time']


            event_comments=item['comments']
            user_utc_date =await self.getDateFromDate(event_action_user_utc_date_time)
            user_utc_time =await self.getTimeFromDatetime(event_action_user_utc_date_time)

            default_work_start_date_time=user_utc_date+" "+default_work_start_time
            default_work_end_date_time = user_utc_date + " " + default_work_end_time

            arrival_date_time=""
            arrival_comments=""
            if self.isArrivalRequest(item['event_name_id']):
                event_comments = await self.getStatusEarlYLate(event_action_user_utc_date_time,default_work_start_date_time)
                arrival_date_time=event_action_user_utc_date_time
                arrival_comments=event_comments

            departure_date_time=""
            departure_comments=""
            if self.isDepartureRequest(item['event_name_id']):
                departure_comments = await self.getStatusEarlYLate(event_action_user_utc_date_time, default_work_end_date_time,True)
                departure_date_time=event_action_user_utc_date_time

            event_text = self.getEventNameByID(item['event_name_id'])

            auto_departure = await self.contains_auto_departure_date(item['auto_departure_user_utc_date_time'])
            if auto_departure:
                missing_event=True
                event_text=" Missing "+event_text



            eventObject = {
                "basic_info": {
                    "time_zone": time_zone,
                    "user_id": user_id,
                    "weekend_id": weekend_id,
                    "default_work_start_time": default_work_start_time,
                    "default_work_end_time": default_work_end_time,
                    "default_work_start_date_time": default_work_start_date_time,
                    "default_work_end_date_time":default_work_end_date_time,
                    "user_arrival_date":user_utc_date,
                    "arrival_date_time": arrival_date_time,
                    "arrival_comments":arrival_comments,
                    "departure_date_time":departure_date_time,
                    "departure_comments": departure_comments



                },
                "data": [{
                    "user_id": item['user_id'],
                    "event_action_type": item['event_action_type'],
                    "event_action_user_utc_date_time": event_action_user_utc_date_time,
                    "event_name_id": item['event_name_id'],
                    "event_text": event_text,
                    "status": item['status'],
                    "event_action_time": user_utc_time,
                    "comments": event_comments,
                    "missing_event": missing_event,
                    "event_start_ip": item['event_start_ip'],
                }]
            }


            if user_utc_date not in source_data:
                source_data[user_utc_date] = eventObject
            else:
                source_data[user_utc_date]["data"].append(eventObject["data"][0])




        return await self.getTimeCalculated(source_data)


    async def getTimeCalculated(self,source_data):
        base_work_time_minutes = 8 * 60
        mainObjectData = {}

        totalSpendWorkingTime = 0
        totalActualWorkingTime=0
        totalActualWorkingDay = 0

        for specificDate, data in source_data.items():
            basic_info = data['basic_info']
            event_data = data['data']
            lunch_break_times=0
            ten_minutes_time=0
            away_time=0
            departure_penalty=0
            task_out_side=0
            total_time_spend=0
            session_status = "Done",

            missing_obj = {
                "user_id": basic_info['user_id'],
                "event_action_type": "",
                "arrival_date_time": basic_info['arrival_date_time'],
                "event_name_id": "",
                "event_text": "",
                "status":False,
                "event_action_time": "",
                "comments": "",
                "event_start_ip": "",
                "missing_event":True
            }

            lunch_break_missing=False
            lunch_break_return_missing = False
            departure_missing=False
            ten_minutes_return_missing=False
            away_return_missing=False
            task_out_side_return_missing=False


            default_work_end_date_time = basic_info['default_work_end_date_time']
            current_user_UTC_date_time = await self.Frz.getDateTimeByUTC(int(basic_info['time_zone']), True)

            isArrivalEvent = await self.getExistedEventDateTime(event_data, self.getArrivalID())


            isLunchBreakEvent = await self.getExistedEventDateTime(event_data, self.getLunchBreakID())
            isLunchBreakReturnEvent = await self.getExistedEventDateTime(event_data, self.getLunchBreakReturnID())

            isDepartureEvent = await self.getExistedEventDateTime(event_data, self.getDepartureID())
            isAutoDeparture = await self.getExistedEventAutoDepartureID(event_data, self.getDepartureID())

            isTenMinutesEvent = await self.getExistedEventDateTime(event_data, self.getTenMinitID())
            isTenMinutesReturnEvent = await self.getExistedEventDateTime(event_data, self.getTenMinitReturnID())

            isAwayEvent = await self.getExistedEventDateTime(event_data, self.getAwayID())
            isAwayReturnEvent = await self.getExistedEventDateTime(event_data, self.getAwayReturnID())

            isTaskOutsideEvent = await self.getExistedEventDateTime(event_data, self.getTaskOutsideID())
            isTaskOutsideReturnEvent = await self.getExistedEventDateTime(event_data, self.getTaskOutsideReturnID())

            if isLunchBreakEvent:
                if isLunchBreakReturnEvent:
                    eps_lunch_break_times = await self.isTimeOver(isLunchBreakReturnEvent, isLunchBreakEvent)
                    if eps_lunch_break_times < self.getRequiredMinimumMinutes(self.getLunchBreakID()):
                        lunch_break_times = self.getRequiredMinimumMinutes(self.getLunchBreakID())
                    else:
                        lunch_break_times = eps_lunch_break_times
                else:
                    if isDepartureEvent or isAutoDeparture:
                        lunch_break_times = self.getRequiredMaximumMinutes(self.getLunchBreakID())
                    else:
                        isSameDate = await self.isSameDate(isArrivalEvent, current_user_UTC_date_time)
                        if isSameDate:
                            lunch_break_times = await self.isTimeOver(current_user_UTC_date_time, isLunchBreakEvent)
                        else:
                            lunch_break_times = self.getRequiredMaximumMinutes(self.getLunchBreakID())









            if isTenMinutesEvent:
                if isTenMinutesReturnEvent:
                    ten_minutes_time = await self.isTimeOver(isTenMinutesReturnEvent,isTenMinutesEvent)

                else:
                    if isDepartureEvent or isAutoDeparture:
                        ten_minutes_time = await self.isTimeOver(isDepartureEvent, isTenMinutesEvent)
                    else:
                        ten_minutes_time = await self.isTimeOver(current_user_UTC_date_time, isTenMinutesEvent)

            if isAwayEvent:
                if isAwayReturnEvent:
                    away_time = await self.isTimeOver(isAwayReturnEvent, isAwayEvent)
                else:
                    if isDepartureEvent or isAutoDeparture:
                        away_time = await self.isTimeOver(isDepartureEvent, isAwayEvent)
                    else:
                        isSameDate = await self.isSameDate(isArrivalEvent, current_user_UTC_date_time)
                        if isSameDate:
                            away_time = await self.isTimeOver(current_user_UTC_date_time, isAwayEvent)
                        else:
                            away_time = self.getRequiredMaximumMinutes(self.getAwayID())

            if isTaskOutsideEvent:
                if isTaskOutsideReturnEvent:
                    task_out_side = await self.isTimeOver(isTaskOutsideReturnEvent, isTaskOutsideEvent)
                else:
                    if isDepartureEvent or isAutoDeparture:
                        task_out_side = await self.isTimeOver(isDepartureEvent, isTaskOutsideEvent)
                    else:
                        isSameDate = await self.isSameDate(isArrivalEvent, current_user_UTC_date_time)
                        if isSameDate:
                            task_out_side = await self.isTimeOver(current_user_UTC_date_time, isTaskOutsideEvent)
                        else:
                            task_out_side = self.getRequiredMaximumMinutes(self.getTaskOutsideID())




            if isArrivalEvent and isDepartureEvent:
                total_time_spend = await self.isTimeOver(isDepartureEvent, isArrivalEvent)

            elif isArrivalEvent and isDepartureEvent==False:
                isSameDate = await self.isSameDate(isArrivalEvent, current_user_UTC_date_time)
                if isSameDate:
                    total_time_spend = await self.isTimeOver(current_user_UTC_date_time, isArrivalEvent)
                else:
                    total_time_spend =-base_work_time_minutes

            isSameDate = await self.isSameDate(isArrivalEvent, current_user_UTC_date_time)
            if isArrivalEvent:

                eps_total_time = await self.isTimeOver(current_user_UTC_date_time, isArrivalEvent)
                if isLunchBreakEvent == False and isDepartureEvent == False:
                    if isSameDate == False:
                        lunch_break_times = self.getRequiredMaximumMinutes(self.getLunchBreakID())
                        departure_penalty = self.getRequiredMaximumMinutes(self.getDepartureID())
                    else:
                        isDayEnd= await self.check_work_end(current_user_UTC_date_time,default_work_end_date_time)
                        if isDayEnd:
                            lunch_break_times = self.getRequiredMaximumMinutes(self.getLunchBreakID())
                            departure_penalty = self.getRequiredMaximumMinutes(self.getDepartureID())




            if isDepartureEvent == False and isSameDate == True:
                session_status = "Active"






            if isLunchBreakEvent==False:
                isSameDate = await self.isSameDate(isArrivalEvent, current_user_UTC_date_time)
                if isSameDate == False or (isDepartureEvent or isAutoDeparture):
                    last_index = await self.get_index_of_event_data(event_data, self.getArrivalID())
                    missing_obj['event_text'] = "Missing Lunch Break"

                    event_data.insert(last_index, missing_obj)
            else:
                if isLunchBreakReturnEvent==False:
                    isSameDate = await self.isSameDate(isArrivalEvent, current_user_UTC_date_time)
                    if isSameDate == False or (isDepartureEvent or isAutoDeparture):
                        last_index = await self.get_index_of_event_data(event_data, self.getLunchBreakID())
                        missing_obj['event_text'] = "Missing Return Lunch Break"
                        event_data.insert(last_index, missing_obj)



            if isTenMinutesEvent:
                if isTenMinutesReturnEvent==False:
                    isSameDate = await self.isSameDate(isArrivalEvent, current_user_UTC_date_time)
                    if isSameDate == False or (isDepartureEvent or isAutoDeparture):
                        last_index = await self.get_index_of_event_data(event_data, self.getTenMinitID())
                        missing_obj['event_text'] = "Missing Return 10 minutes walk"
                        event_data.insert(last_index, missing_obj)



            if isAwayEvent:
                if isAwayReturnEvent==False:
                    isSameDate = await self.isSameDate(isArrivalEvent, current_user_UTC_date_time)
                    if isSameDate == False or (isDepartureEvent or isAutoDeparture):
                        last_index = await self.get_index_of_event_data(event_data, self.getAwayID())
                        missing_obj['event_text'] = "Missing Return Away"
                        event_data.insert(last_index, missing_obj)


            if isTaskOutsideEvent:
                if isTaskOutsideReturnEvent==False:
                    isSameDate = await self.isSameDate(isArrivalEvent, current_user_UTC_date_time)
                    if isSameDate == False or (isDepartureEvent or isAutoDeparture):
                        last_index = await self.get_index_of_event_data(event_data, self.getAwayID())
                        missing_obj['event_text'] = "Missing Return Task outside office"
                        event_data.insert(last_index, missing_obj)






            each_day_actual_working_time=0
            ten_minutes_over = 0

            if (ten_minutes_time > 10):
                ten_minutes_over = ten_minutes_time - 10

            if isDepartureEvent == False and isSameDate == True:
                departure_penalty=0

            if (isDepartureEvent == False and isSameDate == True and isLunchBreakEvent == False):

                lunch_break_times = 0
            elif (isDepartureEvent != False and isSameDate == False and isLunchBreakEvent == False):
                lunch_break_times = self.getRequiredMaximumMinutes(self.getLunchBreakID())


            each_day_actual_working_time = total_time_spend - (lunch_break_times + ten_minutes_over + away_time + departure_penalty)

            totalActualWorkingTime+=each_day_actual_working_time

            totalSpendWorkingTime+=total_time_spend

            totalActualWorkingDay += 1

            departure_comments=""
            if isAutoDeparture:
                departure_comments= await self.getAutoDepartureComments(event_data, self.getDepartureID())





            basic_info['departure_date_time']=isDepartureEvent
            basic_info['departure_comments'] = departure_comments

            basic_info['lunch_break_times'] = lunch_break_times
            basic_info['ten_minutes_time'] = ten_minutes_time
            basic_info['away_time'] = away_time
            basic_info['departure_penalty'] = departure_penalty
            basic_info['task_out_side'] = task_out_side
            basic_info['total_time_spend'] = total_time_spend
            basic_info['session_status'] = session_status

            basic_info['lunch_break_start'] = isLunchBreakEvent
            basic_info['ten_minutes_start'] = isTenMinutesEvent
            basic_info['away_start'] = isAwayEvent
            basic_info['task_out_start'] = isTaskOutsideEvent
            basic_info['current_user_UTC_date_time'] = current_user_UTC_date_time
            basic_info['day_actual_working_time'] = each_day_actual_working_time




            mainObjectData[specificDate] = {
                "basic_info": basic_info,
                "data": event_data
            }

        mainObjectData['total_spend_working_time'] = totalSpendWorkingTime
        mainObjectData['total_actual_working_time']=totalActualWorkingTime
        mainObjectData['total_actual_working_day']=totalActualWorkingDay
        return mainObjectData
