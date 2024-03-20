from pydantic import BaseModel, EmailStr, Field
import re

class RegistrationSkeleton(BaseModel):
    account_type_id: int = Field(..., description="Account type ID")
    office_id: int = Field(..., description="Office ID")
    department_id: int = Field(..., description="Department ID")
    designation_id: int = Field(..., description="Designation ID")
    gender: int = Field(..., description="Gender")

    first_name: str = Field(..., description="First Name (min_length=5, max_length=50)")
    last_name: str = Field(..., description="Last Name (min_length=5, max_length=50)")

    email: EmailStr = Field(..., description="Email")
    mobile_number: str = Field(..., description="Mobile Number")


    username: str = Field(..., description="Username (min_length=5, max_length=20, regex=r'^[\w.-]+$')")
    password: str = Field(..., description="Password (min_length=5, max_length=50)")
    confirmPassword: str = Field(..., description="Confirm Password (min_length=5, max_length=50)")
    terms_condition: int = Field(..., description="Terms and Conditions")


    user_photo: str = Field(..., description="User Photo")
    user_ip: str = Field(..., description="User IP")
    comments: str = Field(..., description="Comments")
    logged_id: str = Field(..., description="Logged ID")

class LoginSkeleton(BaseModel):
    username: str = Field(..., description="Username (min_length=5, max_length=20, regex=r'^[\w.-]+$')")
    password: str = Field(..., description="Password (min_length=5, max_length=50)")
    user_ip: str = Field(..., description="User IP")


class LogOutSkeleton(BaseModel):
    sessionToken: str = Field(..., description="sessionToken (min_length=20, max_length=250")
    user_ip: str = Field(..., description="User IP")


class SendNewPasswordSkeleton(BaseModel):
    user_id: int = Field(..., description="User ID")
    user_ip: str = Field(..., description="User IP")

class ChangePasswordSkeleton(BaseModel):
    email: EmailStr = Field(..., description="User Email")
    current_password: str = Field(..., description="Current Password (min_length=5, max_length=50)")
    new_password: str = Field(..., description="New Password (min_length=5, max_length=50)")
    confirmPassword: str = Field(..., description="Confirm Password (min_length=5, max_length=50)")
    user_ip: str = Field(..., description="User IP")

class ForgetPasswordSkeleton(BaseModel):
    email: EmailStr = Field(..., description="User Email")
    user_ip: str = Field(..., description="User IP")



class ChangeAccountTypeSkeleton(BaseModel):
    user_id: int = Field(..., description="User ID")
    account_type_id: int = Field(..., description="Account type id")
    user_ip: str = Field(..., description="User IP")


class FindUserSkeleton(BaseModel):
    key_data: str = Field(..., description="Name/email/mobile number ")
    user_ip: str = Field(..., description="User IP")


class ShowAccountStatusSkeleton(BaseModel):
    user_id: int = Field(..., description="User ID")
    user_ip: str = Field(..., description="User IP")

class AccountStatusSkeleton(BaseModel):
    user_id: int = Field(..., description="User ID")
    status: int = Field(..., description="Status")
    comments: str = Field(..., description="Comments")
    user_ip: str = Field(..., description="User IP")



class AccountVerificationSkeleton(BaseModel):
    verify_token: str = Field(..., description="account verification token")
    user_ip: str = Field(..., description="User IP")



class Validation:
    @staticmethod
    def registrationRequest(data: RegistrationSkeleton):
        # Call and check validations
        is_valid, errors = Validation.validateRegistration(data)

        # Return validation result and error messages
        if errors:
            return False, errors
        else:
            return True, None


    @staticmethod
    def loginRequest(data: LoginSkeleton):
        # Call and check validations
        is_valid, errors = Validation.validateLogin(data)

        # Return validation result and error messages
        if errors:
            return False, errors
        else:
            return True, None



    @staticmethod
    def sendNewPasswordRequest(data: SendNewPasswordSkeleton):
        # Call and check validations
        is_valid, errors = Validation.validateSendNewPassword(data)

        # Return validation result and error messages
        if errors:
            return False, errors
        else:
            return True, None

    @staticmethod
    def changePasswordRequest(data: ChangePasswordSkeleton):
        # Call and check validations
        is_valid, errors = Validation.validateChangePassword(data)

        # Return validation result and error messages
        if errors:
            return False, errors
        else:
            return True, None

    @staticmethod
    def forgetPasswordRequest(data: ForgetPasswordSkeleton):
        # Call and check validations
        is_valid, errors = Validation.validateForgetPassword(data)

        # Return validation result and error messages
        if errors:
            return False, errors
        else:
            return True, None




    @staticmethod
    def changeAccountTypeRequest(data: ChangeAccountTypeSkeleton):
        # Call and check validations
        is_valid, errors = Validation.validateChangeAccountType(data)

        # Return validation result and error messages
        if errors:
            return False, errors
        else:
            return True, None


    @staticmethod
    def FindUserRequest(data: FindUserSkeleton):
        # Call and check validations
        is_valid, errors = Validation.validateFindUser(data)

        # Return validation result and error messages
        if errors:
            return False, errors
        else:
            return True, None



    @staticmethod
    def logOutRequest(data: LogOutSkeleton):
        # Call and check validations
        is_valid, errors = Validation.validateLogOut(data)

        # Return validation result and error messages
        if errors:
            return False, errors
        else:
            return True, None

    @staticmethod
    def accountVerificationRequest(data: AccountVerificationSkeleton):
        # Call and check validations
        is_valid, errors = Validation.validateAccountVerification(data)

        # Return validation result and error messages
        if errors:
            return False, errors
        else:
            return True, None


    @staticmethod
    def showAccountStatusRequest(data: ShowAccountStatusSkeleton):
        # Call and check validations
        is_valid, errors = Validation.validateShowAccountStatus(data)

        # Return validation result and error messages
        if errors:
            return False, errors
        else:
            return True, None


    @staticmethod
    def accountStatusRequest(data: AccountStatusSkeleton):
        # Call and check validations
        is_valid, errors = Validation.validateAccountStatus(data)

        # Return validation result and error messages
        if errors:
            return False, errors
        else:
            return True, None



# validation method start---------------------------------->
    @classmethod
    def validateRegistration(cls, data: RegistrationSkeleton):
        errors = []

        # Validate integer number

        cls.validate_integer("account_type_id", data.account_type_id, errors)
        cls.validate_integer("office_id",data.office_id, errors)
        cls.validate_integer("designation_id", data.designation_id, errors)
        cls.validate_integer("department_id", data.department_id, errors)
        cls.validate_integer("gender", data.gender, errors)


        cls.validate_name("first_name", data.first_name, errors)
        cls.validate_name("last_name", data.first_name, errors)

        cls.validate_email("email", data.email, errors)
        cls.validate_mobile_number("mobile_number", data.mobile_number, errors)

        cls.validate_username("username", data.username, errors)
        cls.validate_password("password", data.password, errors)
        cls.passwords_match("confirmPassword", data.password, data.confirmPassword, errors)

        cls.validate_integer("terms_condition", data.terms_condition, errors)
        cls.validate_user_ip("user_ip", data.user_ip, errors)


        return not errors, errors

    @classmethod
    def validateLogin(cls, data: LoginSkeleton):
        errors = []

        # Validate integer number


        cls.validate_username("username", data.username, errors)
        cls.validate_password("password", data.password, errors)

        cls.validate_user_ip("user_ip", data.user_ip, errors)

        return not errors, errors

    @classmethod
    def validateLogOut(cls, data: LogOutSkeleton):
        errors = []

        # Validate integer number


        cls.validate_session_token("sessionToken", data.sessionToken, errors)
        cls.validate_user_ip("user_ip", data.user_ip, errors)

        return not errors, errors

    @classmethod
    def validateSendNewPassword(cls, data: SendNewPasswordSkeleton):
        errors = []

        # Validate integer number

        cls.validate_integer("user_id", data.user_id, errors)
        cls.validate_user_ip("user_ip", data.user_ip, errors)

        return not errors, errors

    @classmethod
    def validateChangePassword(cls, data: ChangePasswordSkeleton):
        errors = []

        # Validate integer number
        cls.validate_email("email", data.email, errors)
        cls.validate_password("current_password", data.current_password, errors)
        cls.validate_password("new_password", data.new_password, errors)
        cls.passwords_match("confirmPassword", data.new_password, data.confirmPassword, errors)
        cls.validate_user_ip("user_ip", data.user_ip, errors)

        return not errors, errors

    @classmethod
    def validateForgetPassword(cls, data: ForgetPasswordSkeleton):
        errors = []

        # Validate integer number
        cls.validate_email("email", data.email, errors)
        cls.validate_user_ip("user_ip", data.user_ip, errors)

        return not errors, errors



    @classmethod
    def validateChangeAccountType(cls, data: ChangeAccountTypeSkeleton):
        errors = []

        # Validate integer number
        cls.validate_integer("account_type_id", data.account_type_id, errors)
        cls.validate_integer("user_id", data.user_id, errors)
        cls.validate_user_ip("user_ip", data.user_ip, errors)

        return not errors, errors


    @classmethod
    def validateFindUser(cls, data: FindUserSkeleton):
        errors = []

        # Validate integer number
        cls.validate_search("key_data", data.key_data, errors)
        cls.validate_user_ip("user_ip", data.user_ip, errors)

        return not errors, errors

    @classmethod
    def validateAccountVerification(cls, data: AccountVerificationSkeleton):
        errors = []

        # Validate integer number
        cls.validate_session_token("verify_token", data.verify_token, errors)
        cls.validate_user_ip("user_ip", data.user_ip, errors)

        return not errors, errors

    @classmethod
    def validateShowAccountStatus(cls, data: ShowAccountStatusSkeleton):
        errors = []

        # Validate integer number
        cls.validate_integer("user_id", data.user_id, errors)
        cls.validate_user_ip("user_ip", data.user_ip, errors)

        return not errors, errors

    @classmethod
    def validateAccountStatus(cls, data: AccountStatusSkeleton):
        errors = []

        # Validate integer number

        cls.validate_integer("status", data.status, errors)
        cls.validate_integer("user_id", data.user_id, errors)
        cls.validate_user_ip("user_ip", data.user_ip, errors)

        return not errors, errors


    # global method start------------------------------>
    @classmethod
    def validate_integer(cls, field_name, value, errors):
        if not isinstance(value, int) or value <= 0:
            errors.append({"field": field_name,
                           "message": f"{field_name.replace('_', ' ').capitalize()} must be a positive integer"})

    @classmethod
    def validate_name(cls, field_name, value, errors):
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', value.strip()):
            errors.append({"field": field_name,
                           "message": f"{field_name.replace('_', ' ').capitalize()} must start with a letter and can only contain letters, numbers, and underscores"})

    @classmethod
    def validate_username(cls, field_name, value, errors):
        if len(value.strip()) < 5 or len(value.strip()) > 20:
            errors.append({"field": field_name,
                           "message": f"{field_name.replace('_', ' ').capitalize()} must be between 5 and 20 characters long"})
        elif not re.match(r'^[a-zA-Z][a-zA-Z0-9]*(?:_[a-zA-Z0-9]+)*$', value.strip()):
            errors.append({"field": field_name,
                           "message": f"{field_name.replace('_', ' ').capitalize()} must start with a letter and can only contain letters, numbers, and underscores, with no consecutive underscores and cannot consist solely of numbers"})
    @classmethod
    def validate_password(cls, field_name, password, errors):
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{5,50}$", password.strip()):
            errors.append({"field": field_name,
                           "message": f"{field_name.replace('_', ' ').capitalize()} must contain at least one uppercase letter, one lowercase letter, and one numeric digit, and be between 5 and 50 characters long"})
    @classmethod
    def passwords_match(cls, field_name, password, confirm_password, errors):
        if password.strip() != confirm_password.strip():
            errors.append({"field": field_name, "message": "Passwords does not match"})

    @classmethod
    def validate_email(cls, field_name, email, errors):
        if not re.match(r'^[a-zA-Z0-9._]+@[a-zA-Z0-9._-]+\.[a-zA-Z]{2,}$', email.strip()):
            errors.append({"field": field_name,
                           "message": f"The {field_name.replace('_', ' ')} must be a valid email address"})
        elif len(email.strip()) < 8 or len(email.strip()) > 50:
            errors.append({"field": field_name,
                           "message": f"The {field_name.replace('_', ' ')} must be between 8 and 50 characters long"})
    @classmethod
    def validate_mobile_number(cls, field_name, value, errors):
        if not re.match(r'^\+\d{1,3}\d{6,14}$', value.strip()) or len(value.strip()) < 8 or len(value.strip()) > 20:
            errors.append({"field": field_name,
                           "message": f"{field_name.replace('_', ' ').capitalize()} format is incorrect. It should be in the format: [+][country code][subscriber number] and must be between 8 and 20 characters long."})


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
