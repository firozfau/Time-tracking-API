from datetime import datetime, timedelta
import random
import string

class Frz:
    def __init__(self):
        pass

    def isTestEmail(self,emailKey):
        emailList = ['firozur.rahman@fau.de', 'test@gmail.com']
        trimmedEmailKey = emailKey
        while trimmedEmailKey.startswith(" "):
            trimmedEmailKey = trimmedEmailKey[1:]
        while trimmedEmailKey.endswith(" "):
            trimmedEmailKey = trimmedEmailKey[:-1]
        for email in emailList:
            if email == trimmedEmailKey:
                return True
        return False

    async def getWebSiteLink(self, webKey):
        webList = {
            "web": "http://localhost:8080/",
            "admin": "http://localhost:8080/admin/",
        }
        if webKey:
            if webKey in webList:
                return webList[webKey]
            else:
                return "Gender ID not found"
        else:
            return webList

    async def getGender(self, genderId=False):
        gender_dict = {
            1: "Male",
            2: "Female",
            3: "Others"
        }
        if genderId:
            if genderId in gender_dict:
                return gender_dict[genderId]
            else:
                return "Gender ID not found"
        else:
            return gender_dict

    async def accountStatus(self, statusID=False):
        status_dict = {
            0: "Not-Verified",
            1: "Active",
            2: "Inactive",
            3: "Block",
            4: "Delete"
        }
        if statusID:
            return status_dict.get(statusID, "Status ID not found")
        else:
            return status_dict

    async def accountTypeList(self, statusID=False):
        status_dict = {
            2: "Admin",
            3: "Finance",
            4: "Manager",
            5: "Team leader",
            6: "Reporter",
            7: "Viewer",
            8: "Support",
            9: "Normal user"
        }


        if statusID:
            return status_dict.get(statusID, "Account Type ID not found")
        else:
            return status_dict

    async def userGroup(self, group_id=1):
        group_id_dict = {
            1: "Super admin",
            2: "Admin",
            3: "Manager,Finance,Product Owner Team leader",
            4: "Reporter,Viewer,Support",
            5: "Normal user"
        }
        if group_id:
            return group_id_dict.get(group_id, "Group ID not found")
        else:
            return group_id_dict
    async def defaultUserTypeID(self):
        return 9 # normal user

    async def defaultUserTypeGroupID(self):
        return 5  # normal user

    async def getCurrentDateTime(self):
        return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    async def getCurrentTimeStamp(self):
        return  datetime.now().timestamp()

    async def getAMPMDateTime(self, current_datetime=None):
        if not current_datetime:
            current_datetime = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        elif isinstance(current_datetime, str):
            current_datetime = datetime.fromisoformat(current_datetime)

        dateTimeString = current_datetime.strftime("%I:%M:%S %p")
        return dateTimeString

    async def getDateTimeByUTC(self, utc,isOnlyDate=False):
        # Get the current date and time in UTC
        current_utc_time = datetime.utcnow()

        # Calculate the time difference based on the provided UTC value
        time_difference = timedelta(hours=utc)

        # Convert UTC time to the target time zone
        target_time = current_utc_time + time_difference

        # Format the time as AM/PM
        formatted_time = target_time.strftime("%Y-%m-%d %I:%M:%S %p")

        # Extract date and time components
        current_date = formatted_time.split()[0]
        current_time = formatted_time.split()[1] + " " + formatted_time.split()[2]
        if isOnlyDate==True:
           return formatted_time
        else:
            return {
                "date_time": formatted_time,
                "date": current_date,
                "time": current_time,
                "utc": utc
            }

    async def getFirstDateOfMonthByDate(self,stringDate):
        datetime_str = "2024-05-19 06:01:19 AM"

        # Convert the string to a datetime object
        dt = datetime.strptime(datetime_str, "%Y-%m-%d %I:%M:%S %p")

        # Get the first date of the month
        first_date_of_month = dt.replace(day=1)

        # Convert the first date of the month back to string format
        first_date_of_month_str = first_date_of_month.strftime("%Y-%m-%d")

        return first_date_of_month_str

    async def getLirstDateOfMonthByDate(self, datetime_str):
        import calendar

        dt = datetime.strptime(datetime_str, "%Y-%m-%d %I:%M:%S %p")
        year = dt.year
        month = dt.month
        last_day_of_month = calendar.monthrange(year, month)[1]
        last_date_of_month = dt.replace(day=last_day_of_month)
        last_date_of_month_str = last_date_of_month.strftime("%Y-%m-%d")
        return last_date_of_month_str

    async def isTimeOver(self,current_time_str, base_time_str):
        # Convert time strings to datetime objects
        current_time = datetime.strptime(current_time_str, '%I:%M:%S %p')
        base_time = datetime.strptime(base_time_str, '%I:%M %p')

        # Check if current time is greater than or equal to base time
        if current_time >= base_time:
            return True
        else:
            return False

    from datetime import datetime

    async def isOverDateTime(self, currentDateTimeString, dBDateTimeString, default_time,defaultHours=20):
        try:
            # Convert strings to datetime objects
            current_datetime = datetime.strptime(currentDateTimeString, "%Y-%m-%d %I:%M:%S %p")
            db_datetime = datetime.strptime(dBDateTimeString, "%Y-%m-%d %I:%M:%S %p")

            # Check if dates are the same
            if current_datetime.date() == db_datetime.date():
                # Check if current time is greater than default_time
                default_time = default_time.strip()  # Remove leading/trailing whitespace
                if current_datetime.time() > datetime.strptime(default_time, "%I:%M %p").time():
                    return True
                else:
                    # Check if hours difference is over 20 hours
                    hours_difference = (current_datetime - db_datetime).total_seconds() / 3600
                    if hours_difference >= defaultHours:
                        return True
                    else:
                        return False
            else:
                return True
        except ValueError:
            # Handle parsing errors, return False if there's an issue with datetime parsing
            return False

    async def geRandomPassword(self,digit):
        # Define the pool of characters to choose from
        characters = string.ascii_letters + string.digits

        # Generate a password with 5 characters
        password = ''.join(random.choice(characters) for _ in range(digit))

        # Ensure the password meets the criteria
        while not (any(c.islower() for c in password) and
                   any(c.isupper() for c in password) and
                   any(c.isdigit() for c in password)):
            password = ''.join(random.choice(characters) for _ in range(digit))

        return password

    async def convertIntegerData(self, data):
        try:
            converted_data = int(data)
            return converted_data
        except ValueError:
            return data

    async def getStringFromObject(self,s):
        # Define the symbols to remove
        symbols = {'[', ']', '{', '}', '?', '"', "'", ':'}

        # Initialize an empty list to store processed strings
        processed_strings = []

        # Iterate over each string in the list
        for string in s:
            # Remove symbols from the current string
            for symbol in symbols:
                string = string.replace(symbol, ' ')

            # Add the processed string to the list
            processed_strings.append(string)

        # Join the processed strings and return
        return ' '.join(processed_strings)

    async def getNumberStringFromObject(self,obj):
        number_string = ''
        if isinstance(obj, list):
            # Iterate through the list elements
            for element in obj:
                # Check if the element is numeric
                if isinstance(element, (int, float)):
                    # Append the numeric element to the string
                    number_string += str(element)
        return number_string

    async def isDateFormate(self,date_string):
        try:
            # Split the date string into year, month, and day
            date_parts = str(date_string).split("-")

            # Ensure there are exactly three parts (year, month, day)
            if len(date_parts) != 3:
                return False


            # Check if each part is a valid integer
            try:
                year = int(date_parts[0])
                month = int(date_parts[1])
                day = int(date_parts[2])
            except ValueError:
                return False

            # Check the validity of each part based on your criteria
            if len(date_parts[0]) != 4 or year == 0:
                return False
            if not (1 <= month <= 12):
                return False
            if not (1 <= day <= 31):  # Adjust this range based on your requirements
                return False

            # If all checks pass, the date format is valid
            return True

        except ValueError:
            return False