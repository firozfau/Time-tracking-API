from pydantic import BaseModel, EmailStr, Field
import re,datetime
from datetime import date
from typing import List
import pytz


class ShowReportSkeleton(BaseModel):
    from_date: date = Field(..., description="From date (format: YYYY-MM-DD)")
    to_date: date = Field(..., description="To date (format: YYYY-MM-DD)")
    report_type: str = Field(..., description="date,day,week,month,year")
    user_id: int = Field(..., description="User ID")
    user_ip: str = Field(..., description="User IP")


class TimeSheetSkeleton(BaseModel):
    from_date: date = Field(..., description="From date (format: YYYY-MM-DD)")
    to_date: date = Field(..., description="To date (format: YYYY-MM-DD)")
    type: int = Field(..., description="1=>Specific Office ,2=>Specific user ")
    report_type: str = Field(..., description="date,day,month,year")
    specific_id: int = Field(..., description="user or office id")
    user_ip: str = Field(..., description="User IP")

class CheckIPSkeleton(BaseModel):
    user_ip: str = Field(..., description="User IP")



class UpdateAccountTypesSkeleton(BaseModel):
    access: List[str] = Field(..., description="Access levels")
    account_type_id: int = Field(..., description="Account type ID")
    user_ip: str = Field(..., description="User IP")
    comments: str = Field(..., description="Comments")
    user_id: int = Field(..., description="User ID")

class AddWeekendConfigSkeleton(BaseModel):
    weekend_name: str = Field(..., description="Weekend name")
    day_name_list_id: List[int] = Field(..., description="List of day name IDs")
    comments: str = Field(..., description="Comments")
    user_id: int = Field(..., description="User ID")
    user_ip: str = Field(..., description="User IP")
class UpdateWeekendConfigSkeleton(BaseModel):
    weekend_id: int = Field(..., description="weekend id")
    weekend_name: str = Field(..., description="Weekend name")
    day_name_list_id: List[int] = Field(..., description="List of day name IDs")
    comments: str = Field(..., description="Comments")
    user_id: int = Field(..., description="User ID")
    user_ip: str = Field(..., description="User IP")

class AccessIPListSkeleton(BaseModel):
    office_id: int = Field(..., description="Office ID")
    ip_address: str = Field(..., description="IP address")
    comments: str = Field(..., description="Comments")
    user_id: int = Field(..., description="User ID")
    user_ip: str = Field(..., description="User IP")



class AccessIPUpdateSkeleton(BaseModel):

    access_ip_id: int = Field(..., description="Access IP ID")
    office_id: int = Field(..., description="Office ID")
    ip_address: str = Field(..., description="IP address")
    status: int = Field(..., description="Status")
    comments: str = Field(..., description="Comments")
    user_id: int = Field(..., description="User ID")
    user_ip: str = Field(..., description="User IP")




class OfficeConfigSkeleton(BaseModel):
    country_id: int = Field(..., description="Country ID")
    organization_name: str = Field(..., description="Organization name")
    address: str = Field(..., description="Address")
    main_responsible: str = Field(..., description="main responsible")
    director_name: str = Field(..., description="director name")
    finance_name: str = Field(..., description="finance name")
    hr_name: str = Field(..., description="HR name")
    office_email: EmailStr = Field(..., description="Office Email")
    office_mobile_number: str = Field(..., description="office mobile number")

    default_langauge: int = Field(..., description="default langauge")
    office_start_date: date = Field(..., description="Start date (format: YYYY-MM-DD)")
    default_timezone: str = Field(..., description="default timezone")

    default_work_start_time: str = Field(..., description="Work start time (format: HH:MM:SS AM/PM)")
    default_work_end_time: str = Field(..., description="Work start time (format: HH:MM:SS AM/PM)")
    default_weekend_id: int = Field(..., description="weekend id")
    default_office_ip: str = Field(..., description="Default office IP")
    comments: str = Field(..., description="Comments")


    user_id: int = Field(..., description="User ID")
    user_ip: str = Field(..., description="User IP")



class OfficeConfigUpdateSkeleton(BaseModel):
    office_id: int = Field(..., description="Office ID")
    country_id: int = Field(..., description="Country ID")
    organization_name: str = Field(..., description="Organization name")
    address: str = Field(..., description="Address")
    main_responsible: str = Field(..., description="Main responsible")
    director_name: str = Field(..., description="Director name")
    finance_name: str = Field(..., description="Finance name")
    hr_name: str = Field(..., description="HR name")
    office_email: EmailStr = Field(..., description="Office Email")
    office_mobile_number: str = Field(..., description="Office mobile number")

    default_langauge: int = Field(..., description="default language")
    office_start_date: date = Field(..., description="Start date (format: YYYY-MM-DD)")
    default_timezone: str = Field(..., description="default timezone")

    default_work_start_time: str = Field(..., description="Work start time (format: HH:MM:SS AM/PM)")
    default_work_end_time: str = Field(..., description="Work start time (format: HH:MM:SS AM/PM)")
    default_weekend_id: int = Field(..., description="weekend id")
    default_office_ip: str = Field(..., description="Default office IP")
    comments: str = Field(..., description="Comments")

    user_id: int = Field(..., description="User ID")
    user_ip: str = Field(..., description="User IP")



class ShowHolidayConfigListSkeleton(BaseModel):
    office_id: int = Field(..., description="Office ID")
    user_ip: str = Field(..., description="User IP")


class HolidayConfigSkeleton(BaseModel):
    office_id: int = Field(..., description="Office ID")
    day_id: int = Field(..., description="Day ID")
    month_id: int = Field(..., description="Month ID")
    year: int = Field(..., description="Year")

    comments: str = Field(..., description="Comments")

    user_id: int = Field(..., description="User ID")
    user_ip: str = Field(..., description="User IP")


class HolidayConfigUpdateSkeleton(BaseModel):
    office_holiday_config_id: int = Field(..., description="holiday config ID")
    office_id: int = Field(..., description="Office ID")
    day_id: int = Field(..., description="Day ID")
    month_id: int = Field(..., description="Month ID")
    year: int = Field(..., description="Year")

    comments: str = Field(..., description="Comments")
    status: int = Field(..., description="Status")

    user_id: int = Field(..., description="User ID")
    user_ip: str = Field(..., description="User IP")





class UserConfigListSkeleton(BaseModel):

    user_id: int = Field(..., description="User ID")
    user_ip: str = Field(..., description="User IP")



class UserConfigSkeleton(BaseModel):

    office_id: int = Field(..., description="Office ID")
    user_id: int = Field(..., description="User ID")
    country_id: int = Field(..., description="Country ID")
    time_zone: str = Field(..., description="default timezone")
    joining_date: date = Field(..., description="Joining date (format: YYYY-MM-DD)")
    work_start_time: str = Field(..., description="Work start time (format: HH:MM:SS AM/PM)")
    work_end_time: str = Field(..., description="Work end time (format: HH:MM:SS AM/PM)")
    weekend_id: int = Field(..., description="Weekend Id")

    comments: str = Field(..., description="Comments")
    created_id: int = Field(..., description="Created ID")
    user_ip: str = Field(..., description="User IP")


class UserConfigUpdateSkeleton(BaseModel):
    user_config_id: int = Field(..., description="user config ID")
    office_id: int = Field(..., description="Office ID")
    user_id: int = Field(..., description="User ID")
    country_id: int = Field(..., description="Country ID")
    time_zone: str = Field(..., description="default timezone")
    joining_date: date = Field(..., description="Joining date (format: YYYY-MM-DD)")
    work_start_time: str = Field(..., description="Work start time (format: HH:MM:SS AM/PM)")
    work_end_time: str = Field(..., description="Work end time (format: HH:MM:SS AM/PM)")
    weekend_id: int = Field(..., description="Weekend Id")

    comments: str = Field(..., description="Comments")
    status: int = Field(..., description="Status")

    created_id: int = Field(..., description="Created ID")
    user_ip: str = Field(..., description="User IP")


class Validation:
    @staticmethod
    def ShowReportRequest(data: ShowReportSkeleton):
        # Call and check validations
        is_valid, errors = Validation.validateShowReport(data)

        # Return validation result and error messages
        if errors:
            return False, errors
        else:
            return True, None

    @staticmethod
    def ShowTimeSheetRequest(data: TimeSheetSkeleton):
        # Call and check validations
        is_valid, errors = Validation.validateTimeSheetRequest(data)

        # Return validation result and error messages
        if errors:
            return False, errors
        else:
            return True, None

    @staticmethod
    def checkIPRequest(data: CheckIPSkeleton):
        # Call and check validations
        is_valid, errors = Validation.validateCheckIP(data)

        # Return validation result and error messages
        if errors:
            return False, errors
        else:
            return True, None

    @staticmethod
    def UpdateAccountTypesRequest(data: UpdateAccountTypesSkeleton):
        # Call and check validations
        is_valid, errors = Validation.validateUpdateAccountTypes(data)

        # Return validation result and error messages
        if errors:
            return False, errors
        else:
            return True, None

    @staticmethod
    def AddWeekendConfigRequest(data: AddWeekendConfigSkeleton):
        # Call and check validations
        is_valid, errors = Validation.validateUpdateWeekendConfig(data)

        # Return validation result and error messages
        if errors:
            return False, errors
        else:
            return True, None

    @staticmethod
    def UpdateWeekendConfigRequest(data: UpdateWeekendConfigSkeleton):
        # Call and check validations
        is_valid, errors = Validation.validateUpdateWeekendConfig(data)

        # Return validation result and error messages
        if errors:
            return False, errors
        else:
            return True, None

    @staticmethod
    def AccessIPListRequest(data: AccessIPListSkeleton):
        # Call and check validations
        is_valid, errors = Validation.validateAccessIPList(data)

        # Return validation result and error messages
        if errors:
            return False, errors
        else:
            return True, None

    @staticmethod
    def AccessIPUpdateRequest(data: AccessIPUpdateSkeleton):
        # Call and check validations
        is_valid, errors = Validation.validateAccessIPUpdate(data)

        # Return validation result and error messages
        if errors:
            return False, errors
        else:
            return True, None

    @staticmethod
    def OfficeConfigRequest(data: OfficeConfigSkeleton):
        # Call and check validations
        is_valid, errors = Validation.validateOfficeConfig(data)

        # Return validation result and error messages
        if errors:
            return False, errors
        else:
            return True, None

    @staticmethod
    def OfficeConfigUpdateRequest(data: OfficeConfigUpdateSkeleton):
        # Call and check validations
        is_valid, errors = Validation.validateOfficeConfigUpdate(data)

        # Return validation result and error messages
        if errors:
            return False, errors
        else:
            return True, None



    @staticmethod
    def showHolidayConfigListRequest(data: ShowHolidayConfigListSkeleton):
        # Call and check validations
        is_valid, errors = Validation.validateShowHolidayConfigList(data)

        # Return validation result and error messages
        if errors:
            return False, errors
        else:
            return True, None
    @staticmethod
    def HolidayConfigRequest(data: HolidayConfigSkeleton):
        # Call and check validations
        is_valid, errors = Validation.validateHolidayConfig(data)

        # Return validation result and error messages
        if errors:
            return False, errors
        else:
            return True, None

    @staticmethod
    def holidayConfigUpdateRequest(data: HolidayConfigUpdateSkeleton):
        # Call and check validations
        is_valid, errors = Validation.validateHolidayConfigUpdate(data)

        # Return validation result and error messages
        if errors:
            return False, errors
        else:
            return True, None



    @staticmethod
    def userConfigListRequest(data: UserConfigListSkeleton):
        # Call and check validations
        is_valid, errors = Validation.validateUserConfigList(data)

        # Return validation result and error messages
        if errors:
            return False, errors
        else:
            return True, None

    @staticmethod
    def userConfigRequest(data: UserConfigSkeleton):
        # Call and check validations
        is_valid, errors = Validation.validateUserConfig(data)

        # Return validation result and error messages
        if errors:
            return False, errors
        else:
            return True, None

    @staticmethod
    def userConfigUpdateRequest(data: UserConfigUpdateSkeleton):
        # Call and check validations
        is_valid, errors = Validation.validateUserConfigUpdate(data)

        # Return validation result and error messages
        if errors:
            return False, errors
        else:
            return True, None




# ==========================> check method----------
    @classmethod
    def validateShowReport(cls, data: ShowReportSkeleton):
        errors = []

        # Validate integer number
        cls.validate_integer("user_id", data.user_id, errors)
        cls.validate_user_ip("user_ip", data.user_ip, errors)
        cls.validate_report_type("report_type", data.report_type, errors)
        cls.special_from_validate_date("from_date", data.from_date, errors)
        cls.to_validate_date("to_date", data.to_date,data.from_date, errors)

        return not errors, errors

    @classmethod
    def validateTimeSheetRequest(cls, data: TimeSheetSkeleton):
        errors = []

        # Validate integer number
        cls.validate_specific_id("specific_id", data.specific_id, errors)
        cls.validate_user_ip("user_ip", data.user_ip, errors)
        cls.validate_report_type("report_type", data.report_type, errors)
        cls.validate_specific_type_id("type", data.type, errors)

        cls.validate_date("from_date", data.from_date, errors)
        cls.to_validate_date("to_date", data.to_date,data.from_date, errors)


        return not errors, errors


    @classmethod
    def validateCheckIP(cls, data: CheckIPSkeleton):
        errors = []

        # Validate integer number
        cls.validate_user_ip("user_ip", data.user_ip, errors)
        return not errors, errors



    @classmethod
    def validateUpdateAccountTypes(cls, data: UpdateAccountTypesSkeleton):
        errors = []

        # Validate integer number
        cls.validate_integer("account_type_id", data.account_type_id, errors)
        cls.validate_integer("user_id", data.user_id, errors)
        cls.validate_access("access", data.access, errors)
        cls.validate_user_ip("user_ip", data.user_ip, errors)
        return not errors, errors


    @classmethod
    def validateUpdateWeekendConfig(cls, data: UpdateWeekendConfigSkeleton):
        errors = []

        # Validate integer number
        cls.validate_specialName("weekend_name", data.weekend_name, errors)
        cls.validate_day_list_id("day_name_list_id", data.day_name_list_id, errors)

        cls.validate_string("comments", data.comments, errors)
        cls.validate_integer("user_id", data.user_id, errors)
        cls.validate_user_ip("user_ip", data.user_ip, errors)
        return not errors, errors


    @classmethod
    def validateAccessIPList(cls, data: AccessIPListSkeleton):
        errors = []

        # Validate integer number
        cls.validate_integer("office_id", data.office_id, errors)
        cls.validate_user_ip("ip_address", data.ip_address, errors)
        cls.validate_string("comments", data.comments, errors)

        cls.validate_integer("user_id", data.user_id, errors)
        cls.validate_user_ip("user_ip", data.user_ip, errors)
        return not errors, errors

    @classmethod
    def validateAccessIPUpdate(cls, data: AccessIPListSkeleton):
        errors = []

        # Validate integer number

        cls.validate_integer("access_ip_id", data.access_ip_id, errors)
        cls.validate_integer("office_id", data.office_id, errors)
        cls.validate_user_ip("ip_address", data.ip_address, errors)
        cls.validate_integer("status", data.status, errors)
        cls.validate_string("comments", data.comments, errors)

        cls.validate_integer("user_id", data.user_id, errors)
        cls.validate_user_ip("user_ip", data.user_ip, errors)
        return not errors, errors

    @classmethod
    def validateOfficeConfig(cls, data: OfficeConfigSkeleton):
        errors = []

        # Validate integer number
        cls.validate_integer("country_id", data.country_id, errors)
        cls.validate_specialName("organization_name", data.organization_name, errors)
        cls.validate_specialName("main_responsible", data.main_responsible, errors)
        cls.validate_email("office_email", data.office_email, errors)

        cls.validate_integer("default_langauge", data.default_langauge, errors)
        cls.validate_timezone("default_timezone", data.default_timezone, errors)

        cls.validate_timeAMPM("default_work_start_time", data.default_work_start_time, errors)
        cls.validate_timeAMPM("default_work_end_time", data.default_work_end_time, errors)

        cls.validate_integer("default_weekend_id", data.default_weekend_id, errors)
        cls.validate_user_ip("default_office_ip", data.default_office_ip, errors)



        cls.validate_integer("user_id", data.user_id, errors)
        cls.validate_user_ip("user_ip", data.user_ip, errors)
        return not errors, errors

    @classmethod
    def validateOfficeConfigUpdate(cls, data: OfficeConfigUpdateSkeleton):
        errors = []

        # Validate integer number
        cls.validate_integer("office_id", data.office_id, errors)
        cls.validate_integer("country_id", data.country_id, errors)
        cls.validate_specialName("organization_name", data.organization_name, errors)
        cls.validate_specialName("main_responsible", data.main_responsible, errors)
        cls.validate_email("office_email", data.office_email, errors)

        cls.validate_integer("default_langauge", data.default_langauge, errors)
        cls.validate_timezone("default_timezone", data.default_timezone, errors)

        cls.validate_timeAMPM("default_work_start_time", data.default_work_start_time, errors)
        cls.validate_timeAMPM("default_work_end_time", data.default_work_end_time, errors)

        cls.validate_integer("default_weekend_id", data.default_weekend_id, errors)
        cls.validate_user_ip("default_office_ip", data.default_office_ip, errors)

        cls.validate_integer("user_id", data.user_id, errors)
        cls.validate_user_ip("user_ip", data.user_ip, errors)
        return not errors, errors





    @classmethod
    def validateShowHolidayConfigList(cls, data: ShowHolidayConfigListSkeleton):
        errors = []
        # Validate integer number
        cls.validate_integer("office_id", data.office_id, errors)
        cls.validate_user_ip("user_ip", data.user_ip, errors)
        return not errors, errors

    @classmethod
    def validateHolidayConfig(cls, data: HolidayConfigSkeleton):
        errors = []

        # Validate integer number
        cls.validate_integer("office_id", data.office_id, errors)
        cls.validate_integer("day_id", data.day_id, errors)
        cls.validate_integer("month_id", data.month_id, errors)
        cls.validate_integer("year", data.year, errors)
        cls.validate_integer("user_id", data.user_id, errors)
        cls.validate_user_ip("user_ip", data.user_ip, errors)
        return not errors, errors

    @classmethod
    def validateHolidayConfigUpdate(cls, data: HolidayConfigUpdateSkeleton):
        errors = []

        # Validate integer number
        cls.validate_integer("office_holiday_config_id", data.office_holiday_config_id, errors)
        cls.validate_integer("office_id", data.office_id, errors)
        cls.validate_integer("day_id", data.day_id, errors)
        cls.validate_integer("month_id", data.month_id, errors)
        cls.validate_integer("year", data.year, errors)
        cls.validate_integer("status", data.status, errors)
        cls.validate_integer("user_id", data.user_id, errors)
        cls.validate_user_ip("user_ip", data.user_ip, errors)
        return not errors, errors




    @classmethod
    def validateUserConfigList(cls, data: UserConfigListSkeleton):
        errors = []
        # Validate integer number
        cls.validate_integer("user_id", data.user_id, errors)
        cls.validate_user_ip("user_ip", data.user_ip, errors)
        return not errors, errors


    @classmethod
    def validateUserConfig(cls, data: UserConfigSkeleton):
        errors = []
        # Validate integer number

        cls.validate_integer("office_id", data.office_id, errors)
        cls.validate_integer("user_id", data.user_id, errors)
        cls.validate_integer("country_id", data.country_id, errors)

        cls.validate_timezone("time_zone", data.time_zone, errors)
        cls.validate_date("joining_date", data.joining_date, errors)

        cls.validate_timeAMPM("work_start_time", data.work_start_time, errors)
        cls.validate_timeAMPM("work_end_time", data.work_end_time, errors)

        cls.validate_integer("weekend_id", data.weekend_id, errors)
        cls.validate_string("comments", data.comments, errors)

        cls.validate_integer("created_id", data.created_id, errors)
        cls.validate_user_ip("user_ip", data.user_ip, errors)
        return not errors, errors



    @classmethod
    def validateUserConfigUpdate(cls, data: UserConfigUpdateSkeleton):
        errors = []
        # Validate integer number

        cls.validate_integer("user_config_id", data.user_config_id, errors)
        cls.validate_integer("office_id", data.office_id, errors)
        cls.validate_integer("user_id", data.user_id, errors)
        cls.validate_integer("country_id", data.country_id, errors)

        cls.validate_timezone("time_zone", data.time_zone, errors)
        cls.validate_date("joining_date", data.joining_date, errors)
        cls.validate_timeAMPM("work_start_time", data.work_start_time, errors)
        cls.validate_timeAMPM("work_end_time", data.work_end_time, errors)

        cls.validate_integer("weekend_id", data.weekend_id, errors)
        cls.validate_string("comments", data.comments, errors)
        cls.validate_integer("status", data.status, errors)

        cls.validate_integer("created_id", data.created_id, errors)
        cls.validate_user_ip("user_ip", data.user_ip, errors)
        return not errors, errors






    # global method start------------------------------>
    @classmethod
    def validate_integer(cls, field_name, value, errors):
        if not isinstance(value, int) or value <= 0:
            errors.append({"field": field_name,
                           "message": f"{field_name.replace('_', ' ').capitalize()} must be a positive integer"})

    @classmethod
    def validate_specific_id(cls, field_name, value, errors):
        if not isinstance(value, int) or value <= 0 or value > 2:
            errors.append({"field": field_name,
                           "message": f"{field_name.replace('_', ' ').capitalize()} must be a positive integer 1 or 2 (office or user)"})


    @classmethod
    def validate_specific_type_id(cls, field_name, value, errors):
        if not isinstance(value, int) or value <= 0:
            errors.append({"field": field_name,
                           "message": f"{field_name.replace('_', ' ').capitalize()} must be a positive integer User id or office id"})

    @classmethod
    def validate_timezone(cls, field_name, timezone, errors):
        # Regular expression pattern to match only digits and hyphen
        pattern = r'^[0-9-]+$'

        # Check if the provided timezone matches the pattern
        if not re.match(pattern, timezone):
            errors.append({"field": field_name, "message": f"{field_name} must contain only digits and hyphen"})

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
        elif any(char in session_token for char in ['--', '/', '|', "'", '"', '#']):
            errors.append({"field": field_name, "message": f"{field_name} cannot contain --, /, |, ', \", or #"})


    @classmethod
    def validate_anyName(cls, field_name, session_token, errors):
        if len(session_token) < 20 or len(session_token) > 250:
            errors.append({"field": field_name, "message": f"{field_name} must be between 20 and 250 characters long"})
        elif any(char in session_token for char in ['!', '%', '&', '/', '{', '}', '=', '*', '+', ':', ';', '°', '|', '\\', '?','--', '/', '|', "'", '"', '#','_', '.', "'", '"', ',', '(' , ')']):
            errors.append({"field": field_name, "message": f"{field_name} cannot contain special character"})


    @classmethod
    def validate_specialName(cls, field_name, session_token, errors):
        if len(session_token) < 5 or len(session_token) > 250:
            errors.append({"field": field_name, "message": f"{field_name} must be between 20 and 250 characters long"})
        elif any(char in session_token for char in ['!', '%', '&', '/', '{', '}', '=', '*', '+', ':', ';', '°', '|', '\\', '?','--', '/', '|', "'", '"', '#','_', '.', "'", '"', ',', '(' , ')']):
            errors.append({"field": field_name, "message": f"{field_name} cannot contain special character"})


    @classmethod
    def validate_search(cls, field_name, value, errors):
        if len(value) < 2 or len(value) > 50:
            errors.append({"field": field_name, "message": f"{field_name} must be between 2 and 50 characters long"})
        elif any(char in value for char in ['--', '/', '|', "'", '"', '#']):
            errors.append({"field": field_name, "message": f"{field_name} cannot contain --, /, |, ', \", or #"})

    @classmethod
    def validate_string(cls, field_name, value, errors):
        if len(value) > 250:
            errors.append({"field": field_name, "message": f"{field_name} Max 250 characters long"})
        elif any(char in value for char in ['--', '/', '|', "'", '"', '#','%' ]):
            errors.append({"field": field_name, "message": f"{field_name} cannot contain --, /,% ,|, ', \", or #"})

    @classmethod
    def validate_timeAMPM(cls, field_name, time_str, errors):
        # Regular expression to match the time format
        time_format_regex = r'^((1[0-2]|0?[1-9]):([0-5][0-9]):([0-5][0-9]) ([AaPp][Mm]))$'

        # Check if the provided time string matches the expected format
        if not re.match(time_format_regex, time_str):
            errors.append({"field": field_name, "message": f"{field_name} must be in the format 'HH:MM:SS AM/PM'"})

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
    def special_from_validate_date(cls, field_name, date_obj, errors):
        try:
            # Convert the date object to a string in 'YYYY-MM-DD' format
            date_str = date_obj.strftime('%Y-%m-%d')

            # Convert the date string to a datetime object
            date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')

            # Get the current date
            current_date = datetime.datetime.now().date()


        except ValueError:
            # If the date string is not in the correct format, add an error
            errors.append({"field": field_name, "message": f"{field_name} must be in the format 'YYYY-MM-DD'"})

    @classmethod
    def to_validate_date(cls, field_name, date_obj, from_date, errors):
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


    @classmethod
    def validate_report_type(cls, field_name, report_type, errors):
        # Extract allowed values from field description
        description = ShowReportSkeleton.__fields__[field_name].field_info.description
        valid_types = [x.strip() for x in description.split(',')]

        if report_type not in valid_types:
            errors.append(
                {"field": field_name, "message": f"{field_name.capitalize()} must be one of {', '.join(valid_types)}"})


    @classmethod
    def validate_access(cls, field_name, access, errors):
        if not isinstance(access, list):
            errors.append({"field": field_name, "message": "Access must be a list of strings"})
        return access

    @classmethod
    def validate_day_list_id(cls, field_name, value, errors):
        if not isinstance(value, list):
            errors.append({"field": field_name, "message": "All items in day ID must be integers"})
        return value

    @classmethod
    def validate_work_start_time(cls, field_name, time_str, errors):
        if not re.match(r'^(0?[1-9]|1[0-2]):([0-5]\d):([0-5]\d) (AM|PM)$', time_str):
            errors.append({"field": field_name, "message": f"{field_name} must be in the format 'HH:MM:SS AM/PM'"})