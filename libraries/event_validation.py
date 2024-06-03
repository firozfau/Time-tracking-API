from pydantic import BaseModel, EmailStr, Field
import re,datetime
from datetime import date

class EventActionSkeleton(BaseModel):

    user_id: int = Field(..., description="User ID")
    event_name_id: int = Field(..., description="Event name ID")
    sessionToken: str = Field(..., description="sessionToken (min_length=20, max_length=250")
    comments: str = Field(..., description="Comments")
    user_ip: str = Field(..., description="User IP")

class ActiveEventSkeleton(BaseModel):
    user_id: int = Field(..., description="User ID")
    sessionToken: str = Field(..., description="sessionToken (min_length=20, max_length=250")
    user_ip: str = Field(..., description="User IP")

class ShowEventSkeleton(BaseModel):
    from_date: date = Field(..., description="From date (format: YYYY-MM-DD)")
    to_date: date = Field(..., description="To date (format: YYYY-MM-DD)")
    user_id: int = Field(..., description="User ID")
    user_ip: str = Field(..., description="User IP")




class Validation:
    @staticmethod
    def EventActionRequest(data: EventActionSkeleton):
        # Call and check validations
        is_valid, errors = Validation.validateEventAction(data)

        # Return validation result and error messages
        if errors:
            return False, errors
        else:
            return True, None

    @staticmethod
    def ActiveEventRequest(data: ActiveEventSkeleton):
        # Call and check validations
        is_valid, errors = Validation.validateActiveEvent(data)

        # Return validation result and error messages
        if errors:
            return False, errors
        else:
            return True, None

    @staticmethod
    def ShowEventRequest(data: ShowEventSkeleton):
        # Call and check validations
        is_valid, errors = Validation.validateShowEvent(data)

        # Return validation result and error messages
        if errors:
            return False, errors
        else:
            return True, None



# validation method start---------------------------------->

    @classmethod
    def validateEventAction(cls, data: EventActionSkeleton):
        errors = []

        # Validate integer number

        cls.validate_session_token("sessionToken", data.sessionToken, errors)
        cls.validate_integer("user_id", data.user_id, errors)
        cls.validate_integer("event_name_id", data.event_name_id, errors)
        cls.validate_user_ip("user_ip", data.user_ip, errors)

        return not errors, errors

    @classmethod
    def validateActiveEvent(cls, data: ActiveEventSkeleton):
        errors = []

        # Validate integer number
        cls.validate_integer("user_id", data.user_id, errors)
        cls.validate_session_token("sessionToken", data.sessionToken, errors)
        cls.validate_user_ip("user_ip", data.user_ip, errors)

        return not errors, errors


    @classmethod
    def validateShowEvent(cls, data: ShowEventSkeleton):
        errors = []

        # Validate integer number
        cls.validate_integer("user_id", data.user_id, errors)
        cls.validate_user_ip("user_ip", data.user_ip, errors)

        cls.validate_date("from_date", data.from_date, errors)
        cls.to_validate_date("to_date", data.to_date,data.from_date ,errors)
        return not errors, errors










    # global method start------------------------------>
    @classmethod
    def validate_integer(cls, field_name, value, errors):
        if not isinstance(value, int) or value <= 0:
            errors.append({"field": field_name,
                           "message": f"{field_name.replace('_', ' ').capitalize()} must be a positive integer"})

    @classmethod
    def validate_email(cls, field_name, email, errors):
        if not re.match(r'^[a-zA-Z0-9._]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}$', email.strip()):
            errors.append({"field": field_name,
                           "message": f"{field_name.replace('_', ' ').capitalize()} must be a valid email address"})
        elif len(email.strip()) < 8 or len(email.strip()) > 50:
            errors.append({"field": field_name,
                           "message": f"{field_name.replace('_', ' ').capitalize()} must be between 8 and 50 characters long"})

    @classmethod
    def validate_user_ip(cls, field_name, user_ip, errors):
        if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', user_ip):
            errors.append({"field": field_name,
                           "message": f"{field_name} format is incorrect. It should be in the format: xxx.xxx.xxx.xxx"})

    @classmethod
    def validate_session_token(cls, field_name, session_token, errors):
        if len(session_token) < 20 or len(session_token) > 250:
            errors.append({"field": field_name, "message": f"{field_name} must be between 20 and 250 characters long"})
        elif any(char in session_token for char in ['--', '//', '|', "'", '"', '#']):
            errors.append({"field": field_name, "message": f"{field_name} cannot contain --, //, |, ', \", or #"})

    @classmethod
    def validate_search(cls, field_name, session_token, errors):
        if len(session_token) < 2 or len(session_token) > 50:
            errors.append({"field": field_name, "message": f"{field_name} must be between 2 and 50 characters long"})
        elif any(char in session_token for char in ['--', '/', '|', "'", '"', '#']):
            errors.append({"field": field_name, "message": f"{field_name} cannot contain --, /, |, ', \", or #"})



    @classmethod
    def validate_date(cls, field_name, date_obj, errors):
        try:
            # Convert the date object to a string in 'YYYY-MM-DD' format
            date_str = date_obj.strftime('%Y-%m-%d')

            # Convert the date string to a datetime object
            date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')

            # Get the current date
            current_date = datetime.datetime.now().date()

            # Check if the date is in the past or today
            if date_obj.date() > current_date:
                errors.append({"field": field_name, "message": f"{field_name} cannot be in the future"})
        except ValueError:
            # If the date string is not in the correct format, add an error
            errors.append({"field": field_name, "message": f"{field_name} must be in the format 'YYYY-MM-DD'"})

    @classmethod
    def to_validate_date(cls, field_name, date_obj,from_date,errors):
        try:
            # Convert the date object to a string in 'YYYY-MM-DD' format
            date_str = date_obj.strftime('%Y-%m-%d')
            from_date_obj = from_date.strftime('%Y-%m-%d')

            # Convert the date string to a datetime object
            date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
            date_obj_from = datetime.datetime.strptime(from_date_obj, '%Y-%m-%d')

            # Get the current date
            current_date = datetime.datetime.now().date()
            if date_obj.date() < date_obj_from.date():
                errors.append({"field": field_name, "message": f"The to date cannot be smaller than the form date"})
        except ValueError:
            # If the date string is not in the correct format, add an error
            errors.append({"field": field_name, "message": f"{field_name} must be in the format 'YYYY-MM-DD'"})

