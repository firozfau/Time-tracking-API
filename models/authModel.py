
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text
from dbConnection.dbcon import SessionLocal
from libraries.jsonFormate import JsonFormate
from libraries.frz import  Frz
import re
class AuthModel:
    def __init__(self):
        self.DB = SessionLocal()
        self.JSON = JsonFormate()
        self.Frz = Frz()
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






    async def byUsername(self, data):

        sqlQuery = text(
            """
            SELECT *  from users where username=:username order by id desc limit 1
            """
        )

        result=  self.DB.execute(sqlQuery, {"username": data.username})
        resultData = result.fetchall()

       # data = result.fetchall()  # result.fetchall()
        if resultData:
            edata= await self.fetchData(result, resultData)
            return edata
        else:
            return False

    async def byEmail(self, data):

        sqlQuery = text(
            """
            SELECT *  from users where email=:email order by id desc limit 1
            """
        )

        result=  self.DB.execute(sqlQuery, {"email": data.email})
        resultData = result.fetchall()

       # data = result.fetchall()  # result.fetchall()
        if resultData:
            edata=await self.fetchData(result, resultData)
            return edata
        else:
            return False

    async def byUserId(self, data):

        sqlQuery = text(
            """
            SELECT *  from users where id=:user_id order by id desc limit 1
            """
        )

        result=  self.DB.execute(sqlQuery, {"user_id": data.user_id})
        resultData = result.fetchall()

       # data = result.fetchall()  # result.fetchall()
        if resultData:
            edata=await self.fetchData(result, resultData)
            return edata
        else:
            return False



    async def byUserOpenKey(self, optionString,keyText):

        if keyText=="email":

            sqlQuery = text(
                """
                SELECT *  from users where email=:optionString order by id desc limit 1
                """
            )

        elif keyText=="user":
            sqlQuery = text(
                """
                SELECT *  from users where username=:optionString order by id desc limit 1
                """
            )
        else:
            sqlQuery = text(
                """
                SELECT *  from users where id=:optionString order by id desc limit 1
                """
            )

        result = self.DB.execute(sqlQuery, {"optionString": optionString})
        resultData = result.fetchone()

        # data = result.fetchall()  # result.fetchall()
        if resultData:
            return self.JSON.getEncodeData(resultData)
        else:
            return False

    async def getLoginHistoryByID(self, user_id,status):

        sqlQuery = text(
            """
            SELECT *  from login_history where user_id=:user_id and status=:status order by id desc limit 1
            """
        )

        result = self.DB.execute(sqlQuery, {"user_id": user_id,"status": status})
        resultData = result.fetchone()

        # data = result.fetchall()  # result.fetchall()
        if resultData:
            return self.JSON.getEncodeData(resultData)
        else:
            return False

    async def matchWhiteIP(self, requestedIP):

        sqlQuery = text(
            """
            SELECT *  from tts_access_ip_list where ip_address=:ip_address order by id desc limit 1
            """
        )

        result=  self.DB.execute(sqlQuery, {"ip_address": requestedIP})
        resultData = result.fetchone()

       # data = result.fetchall()  # result.fetchall()
        if resultData:
            return self.JSON.getEncodeData(resultData)
        else:
            return False
#================================= insert data ================================================


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



    async def userRegistration(self, data,objectData):

        sqlQuery = text(
            """
            INSERT INTO users (`account_type_id`, `office_id`, `department_id`, `designation_id`, `gender`, `first_name`, `last_name`, `email`, `mobile_number`, `terms_condition`, `user_ip`, `comments`, `user_photo`, `username`, `password`, `verify_token`, `created_id`, `acc_verify_comments`,`email_verify_status`,`status`)
            VALUES (:account_type_id, :office_id, :department_id, :designation_id, :gender, :first_name, :last_name, :email, :mobile_number, :terms_condition, :user_ip, :comments, :user_photo, :username, :password, :verify_token, :created_id,:acc_verify_comments,:email_verify_status,:status)
            """
        )





        result=  self.DB.execute(sqlQuery,
                                 {
                                     'user_group_id': objectData['user_group_id'],
                                     'account_type_id': objectData['account_type_id'],
                                     'office_id': data.office_id,
                                     'department_id': data.department_id,
                                     'designation_id': data.designation_id,
                                     'gender': data.gender,
                                     'first_name': data.first_name,
                                     'last_name': data.last_name,
                                     'email': data.email,
                                     'mobile_number': data.mobile_number,
                                     'terms_condition': data.terms_condition,
                                     'user_ip': data.user_ip,
                                     'comments': data.comments,
                                     'user_photo': data.user_photo,
                                     'username': data.username,
                                     'password': objectData['encrypted_password'],
                                     'verify_token': objectData['verify_token'],
                                     'created_id': data.logged_id,
                                     'acc_verify_comments':"Default verified",
                                     'status':1,
                                     'email_verify_status':1

                                 }
                                 )
        last_insert_id = result.lastrowid

       # data = result.fetchall()  # result.fetchall()
        if last_insert_id:
            return last_insert_id
        else:
            return False




    async def userLoginInsert(self, data,objectData):

        sqlQuery = text(
            """
            INSERT INTO login_history (`user_id`,`sessionToken`,`user_ip`,`comments`,`user_utc_login_time`)
            VALUES (:user_id, :sessionToken, :user_ip, :comments, :user_utc_login_time)
            """
        )

        result=  self.DB.execute(sqlQuery,
                                 {
                                     'user_id': data.user_id,
                                     'sessionToken': data.sessionToken,
                                     'user_ip': data.user_ip,
                                     'comments': data.comments,
                                     'user_utc_login_time':data.user_utc_login_time
                                 }
                                 )
        last_insert_id = result.lastrowid

       # data = result.fetchall()  # result.fetchall()
        if last_insert_id:
            return last_insert_id
        else:
            return False

#================================= updated data ================================================
    async def updateSingleValueOfUser(self, user_id, keyIndex, keyValue):
        try:
            #self.DB.begin()

            sql_query = text(
                "UPDATE users SET {} = :keyValue  WHERE  id = :user_id".format(keyIndex)
            )
            result = self.DB.execute(sql_query, {"keyValue": keyValue, "user_id": user_id})

            self.DB.commit()

            if result.rowcount > 0:
                return "success"
            else:
                return "failed"

        except IntegrityError as e:
            self.DB.rollback()
            return "failed"
        except Exception as e:
            self.DB.rollback()
            print(f"Error: {e}")
            return "error"

        finally:
            self.DB.close()

    async def userLoginUpdate(self, user_id,user_utc_logout_time,logout_by=1,comments=""):
        try:
            #self.DB.begin()

            sql_query = text(
                "UPDATE login_history SET `user_utc_logout_time` = :user_utc_logout_time,`logout_by` = :logout_by, `comments` = :comments ,`status` = 2 WHERE user_id = :user_id"
            )

            #print(user_utc_logout_time,"-->",comments,"==>",logout_by,"-->",user_id)
            result = self.DB.execute(sql_query, {
                'user_utc_logout_time': user_utc_logout_time,
                'user_id': user_id,
                'logout_by': logout_by,
                'comments': comments,
            })

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



#================================= base query data ================================================

    async def getUserTTSConfigInformation(self, user_id):
        try:

            sql_query = text(""" 
            SELECT 
            :isUserTTSConfig as isUserTTSConfig,
            tts_user_config.office_id, tts_user_config.user_id,tts_user_config.joining_date,

            IF((tts_user_config.country_id), tts_user_config.country_id, (tts_office_config.country_id)) country_id,
            
            IF((tts_user_config.time_zone), tts_user_config.time_zone, (tts_office_config.default_timezone)) time_zone,
            IF((tts_user_config.work_start_time), tts_user_config.work_start_time, (tts_office_config.default_work_start_time)) work_start_time,
            IF((tts_user_config.work_end_time), tts_user_config.work_end_time, (tts_office_config.default_work_end_time)) work_end_time,
            
            IF((tts_user_config.weekend_id), tts_user_config.weekend_id, (tts_office_config.default_weekend_id)) weekend_id,
            tts_office_config.organization_name,tts_office_config.address office_address,
            tts_office_config.office_email,tts_office_config.office_mobile_number,
            tts_office_config.default_langauge,
            tts_office_config.default_timezone,
            tts_office_config.default_work_start_time,
            tts_office_config.default_work_end_time,
            tts_office_config.default_weekend_id,
            tts_office_config.default_office_ip,
            tts_office_config.country_id default_country_id 
            
            from tts_user_config 
            INNER JOIN tts_office_config on tts_user_config.office_id=tts_office_config.id
            where tts_user_config.user_id=:user_id ORDER BY tts_user_config.id DESC limit 1
            """)


            result = self.DB.execute(sql_query, {"isUserTTSConfig": True,"user_id": user_id})
            resultData = result.fetchone()
            if resultData:
                return self.JSON.getEncodeData(resultData)
            else:
               dataUsers= await self.byUserOpenKey(user_id, "id")


               if dataUsers:
                    office_id = self.JSON.getDecodedData(dataUsers).get('data')['office_id']

                    isOfficeTTSdata= await  self.getDefaultUserTTSConfigInformation(user_id,office_id)
                    return isOfficeTTSdata
               else:
                   return False
        finally:
            self.DB.close()

    async def getDefaultUserTTSConfigInformation(self, request_user_id,office_id):
        try:

            sql_query = text(""" 
               SELECT 
                :isUserTTSConfig as isUserTTSConfig,
                tts_office_config.id office_id,
                :request_user_id as user_id,
                tts_office_config.created_at joining_date,
                tts_office_config.country_id country_id,
                tts_office_config.default_timezone time_zone,
                tts_office_config.default_work_start_time work_start_time,
                tts_office_config.default_work_end_time work_end_time,
                tts_office_config.default_weekend_id weekend_id,
                tts_office_config.organization_name,
                tts_office_config.address office_address,
                tts_office_config.office_email,tts_office_config.office_mobile_number,
                tts_office_config.default_langauge,
                tts_office_config.default_timezone,
                tts_office_config.default_work_start_time,
                tts_office_config.default_work_end_time,
                tts_office_config.default_weekend_id,
                tts_office_config.default_office_ip,
                tts_office_config.country_id default_country_id

                from tts_office_config
                where tts_office_config.id=:office_id
                ORDER BY tts_office_config.id DESC limit 1
              """)

            result = self.DB.execute(sql_query, {"isUserTTSConfig":False,"request_user_id": request_user_id,"office_id": office_id})
            resultData = result.fetchone()
            if resultData:
                return self.JSON.getEncodeData(resultData)
            else:

                return False
        finally:
            self.DB.close()


    async def loginDataByToken(self,sessionToken,user_id):
        try:

            sql_query = text(
                "SELECT * FROM login_history WHERE sessionToken=:sessionToken and status=1 ORDER BY id DESC limit 1")
            result = self.DB.execute(sql_query, {"sessionToken": sessionToken})
            resultData = result.fetchone()
            if resultData:
                return self.JSON.getEncodeData(resultData)
            else:
                if user_id!=False:
                    return await self.anyLoginHistoryTokenId(sessionToken,user_id)
                else:
                    return False
        finally:
            self.DB.close()

    async def activeLoginHistoryTokenId(self,sessionToken,user_id):
        try:
            sql_query = text(
                "SELECT * FROM login_history WHERE sessionToken=:sessionToken and user_id=:user_id and status=1 ORDER BY id DESC limit 1")
            result = self.DB.execute(sql_query, {"sessionToken": sessionToken,"user_id": user_id})
            resultData = result.fetchone()
            if resultData:
                return self.JSON.getEncodeData(resultData)
            else:
                return False
        finally:
            self.DB.close()

    async def anyLoginHistoryTokenId(self,sessionToken,user_id):
        try:
            sql_query = text(
                "SELECT * FROM login_history WHERE sessionToken=:sessionToken and user_id=:user_id  ORDER BY id DESC limit 1")
            result = self.DB.execute(sql_query, {"sessionToken": sessionToken,"user_id": user_id})
            resultData = result.fetchone()

            if resultData:
                return self.JSON.getEncodeData(resultData)
            else:
                return False
        finally:
            self.DB.close()

    async def findUsers(self, search_data):
        try:
            sql_query = text(
                "SELECT username,user_ip,first_name,last_name,email,mobile_number,user_photo,office_id,department_id,designation_id,gender FROM users WHERE username LIKE :search_data OR email LIKE :search_data OR first_name LIKE :search_data OR last_name LIKE :search_data OR mobile_number LIKE :search_data ORDER BY id DESC")
            result = self.DB.execute(sql_query, {"search_data": f"%{search_data}%"})
            data = result.fetchall()  # result.fetchall()
            if data:
                return await self.fetchData(result, data)
            else:
                return False
        finally:
            self.DB.close()