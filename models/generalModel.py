#generalModel.py
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text
from dbConnection.dbcon import SessionLocal
from libraries.jsonFormate import JsonFormate
from libraries.frz import  Frz

class GeneralModel:
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



    async def getAccountTypeById(self, data):

        sqlQuery = text(
            """
            SELECT *  from account_type where id=:id order by id desc limit 1
            """
        )

        result=  self.DB.execute(sqlQuery, {"id": data.id})
        resultData = result.fetchone()

       # data = result.fetchall()  # result.fetchall()
        if resultData:
            return self.JSON.getEncodeData(resultData)
        else:
            return False

    async def dayNameList(self, data):

        sqlQuery = text(
            """
            SELECT *  from day_name_list where status=1 
            """
        )

        result=  self.DB.execute(sqlQuery)
        resultData =result.fetchall()
        if resultData:
            return await self.fetchData(result, resultData)
        else:
            return False

    async def monthNameList(self, data):

        sqlQuery = text(
            """
            SELECT *  from month_name_list where status=1 
            """
        )

        result=  self.DB.execute(sqlQuery)
        resultData =result.fetchall()
        if resultData:
            return await self.fetchData(result, resultData)
        else:
            return False

    async def weekendById(self, data):

        sqlQuery = text(
            """
            SELECT *  from weekend_list where id=:weekend_id
            """
        )

        result=  self.DB.execute(sqlQuery,{"weekend_id":data.weekend_id})
        resultData =result.fetchall()
        if resultData:
            return await self.fetchData(result, resultData)
        else:
            return False

    async def weekendList(self, data):

        sqlQuery = text(
            """
            SELECT *  from weekend_list
            """
        )

        result=  self.DB.execute(sqlQuery)
        resultData =result.fetchall()
        if resultData:
            return await self.fetchData(result, resultData)
        else:
            return False

    async def countryNameList(self, data):

        sqlQuery = text(
            """
            SELECT *  from countries_list order by  status DESC
            """
        )

        result = self.DB.execute(sqlQuery)
        resultData = result.fetchall()
        if resultData:
            return await self.fetchData(result, resultData)
        else:
            return False

    async def departmentNameList(self, data):

        sqlQuery = text(
            """
            SELECT *  from department_list where status=1
            """
        )

        result = self.DB.execute(sqlQuery)
        resultData = result.fetchall()
        if resultData:
            return await self.fetchData(result, resultData)
        else:
            return False


    async def designationNameList(self, data):

        sqlQuery = text(
            """
            SELECT *  from designation_list where status=1
            """
        )

        result = self.DB.execute(sqlQuery)
        resultData = result.fetchall()
        if resultData:
            return await self.fetchData(result, resultData)
        else:
            return False


    async def userAllList(self, data):

        sqlQuery = text(
            """
           SELECT 
                    users.id,
                    users.user_group_id,
                    users.account_type_id,
                    users.office_id,
                    users.username,
                    users.email,
                    users.first_name,
                    users.last_name,
                    users.department_id,
                    users.designation_id,
                    users.gender,
                    users.mobile_number,
                    users.user_photo,
                    users.`status`,
                    users.email_verify_status,
                    users.comments,
                    users.terms_condition,
                    users.user_ip,
                    department_list.department_name,
                    designation_list.designation_name,
                    tts_office_config.organization_name,
                    account_type.`name` AS account_type_name
                FROM 
                    users
                INNER JOIN 
                    department_list ON users.department_id = department_list.id
                INNER JOIN 
                    designation_list ON users.designation_id = designation_list.id
                INNER JOIN 
                    tts_office_config ON users.office_id = tts_office_config.id
                INNER JOIN 
                    account_type ON users.account_type_id = account_type.id
                WHERE 
                    users.account_type_id != 1 
                ORDER BY 
                    users.id DESC;

            """
        )

        result = self.DB.execute(sqlQuery)
        resultData = result.fetchall()
        if resultData:
            return await self.fetchData(result, resultData)
        else:
            return False

    async def accessIPList(self, data):

        sqlQuery = text(
            """
                       SELECT 
                        tts_access_ip_list.*,
                        tts_office_config.organization_name,
                        tts_office_config.country_id,
                        tts_office_config.address,
                        tts_office_config.default_langauge,
                        tts_office_config.default_timezone,
                        tts_office_config.default_weekend_id,
                        tts_office_config.default_work_start_time,
                        tts_office_config.default_work_end_time
                    FROM 
                        tts_access_ip_list
                    INNER JOIN 
                        tts_office_config ON tts_access_ip_list.office_id = tts_office_config.id
                    ORDER BY 
                        tts_access_ip_list.id DESC;

            """
        )

        result = self.DB.execute(sqlQuery)
        resultData = result.fetchall()
        if resultData:
            return await self.fetchData(result, resultData)
        else:
            return False

    async def weekendListByName(self, data):

        weekend_name = data.weekend_name
        weekendNameString = weekend_name.lower().replace(" ", "")


        sqlQuery = text(
            """
           SELECT * FROM weekend_list WHERE REPLACE(LOWER(weekend_name), ' ', '')=:weekend_name
            """
        )

        result=  self.DB.execute(sqlQuery,{"weekend_name":weekendNameString})
        resultData =result.fetchall()
        if resultData:
            return await self.fetchData(result, resultData)
        else:
            return False

    async def updateAccountAccess(self,account_type_id,access,status,comments,updated_id,last_ip):
        try:
            #self.DB.begin()

            sql_query = text(
                "UPDATE account_type SET `access` = :access,`status` = :status,`comments` = :comments,`updated_id` = :updated_id,`last_ip` = :last_ip  WHERE id = :account_type_id"
            )
            result = self.DB.execute(sql_query, {
                'access': access,
                'account_type_id': account_type_id,
                'status': status,
                'comments': comments,
                'updated_id': updated_id,
                'last_ip': last_ip
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



    async def addWeekend(self, data,objectData):

        sqlQuery = text(
            """
            INSERT INTO weekend_list (`weekend_name`, `day_name_list_id`, `comments`, `created_id`, `user_ip`)
            VALUES (:weekend_name, :day_name_list_id, :comments, :created_id, :user_ip)
            """
        )
        result=  self.DB.execute(sqlQuery,
                                 {
                                     'weekend_name': data.weekend_name,
                                     'day_name_list_id': data.day_name_list_id,
                                     'comments': data.comments,
                                     'created_id': data.created_id,
                                     'user_ip': data.user_ip

                                 }
                                 )
        last_insert_id = result.lastrowid

       # data = result.fetchall()  # result.fetchall()
        if last_insert_id:
            return last_insert_id
        else:
            return False





    async def updateWeekend(self,weekend_id,weekend_name,day_name_list_id,comments,user_id,user_ip):
        try:
            #self.DB.begin()

            sql_query = text(
                "UPDATE weekend_list SET `weekend_name` = :weekend_name, `day_name_list_id` = :day_name_list_id, `comments` = :comments, `updated_id` = :updated_id, `user_ip` = :user_ip WHERE id = :weekend_id"
            )
            result = self.DB.execute(sql_query, {

                'weekend_id': weekend_id,
                'weekend_name': weekend_name,
                'day_name_list_id': day_name_list_id,
                'comments': comments,
                'updated_id': user_id,
                'user_ip': user_ip
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




    async def addAccessIPList(self, data,objectData):

        sqlQuery = text(
            """
            INSERT INTO tts_access_ip_list (`office_id`, `ip_address`, `comments`, `created_id`, `user_ip`)
            VALUES (:office_id, :ip_address, :comments, :created_id, :user_ip)
            """
        )
        #print(data.ip_address)

        result=  self.DB.execute(sqlQuery,
                                 {
                                     'office_id': data.office_id,
                                     'ip_address': data.ip_address,
                                     'comments': data.comments,
                                     'created_id': data.user_id,
                                     'user_ip': data.user_ip

                                 }
                                 )
        last_insert_id = result.lastrowid

       # data = result.fetchall()  # result.fetchall()
        if last_insert_id:
            return last_insert_id
        else:
            return False

    async def getOfficeInfoById(self, office_id):

        sqlQuery = text(
            """
            SELECT *  from tts_office_config where id=:office_id order by id desc limit 1
            """
        )

        result=  self.DB.execute(sqlQuery, {"office_id": office_id})
        resultData = result.fetchone()

       # data = result.fetchall()  # result.fetchall()
        if resultData:
            return self.JSON.getEncodeData(resultData)
        else:
            return False

    async def getAccessIPInfoById(self, access_ip_id):

        sqlQuery = text(
            """
            SELECT *  from tts_access_ip_list where id=:access_ip_id order by id desc limit 1
            """
        )

        result=  self.DB.execute(sqlQuery, {"access_ip_id": access_ip_id})
        resultData = result.fetchone()

       # data = result.fetchall()  # result.fetchall()
        if resultData:
            return self.JSON.getEncodeData(resultData)
        else:
            return False

    async def updateAccessIPList(self, data):
        try:
            # self.DB.begin()

            sql_query = text(
                "UPDATE tts_access_ip_list SET `office_id` = :office_id,`ip_address` = :ip_address,`status` = :status,`comments` = :comments,`user_ip` = :user_ip,`updated_id` = :updated_id  WHERE id = :access_ip_id"
            )
            result = self.DB.execute(sql_query, {

                'access_ip_id': data.access_ip_id,
                'office_id': data.office_id,
                'ip_address': data.ip_address,
                'status': data.status,
                'comments': data.comments,
                'user_ip': data.user_ip,
                'updated_id':data.user_id


            })

            self.DB.commit()

            if result.rowcount > 0:
                return "success"
            else:
                return "failed"

        except IntegrityError as e:
            # self.DB.rollback()
            return "failed"
        except Exception as e:
            # self.DB.rollback()
            # print(f"Error: {e}")
            return "error"

        finally:
            self.DB.close()


    async def officeList(self, data):

        sqlQuery = text(
            """
           SELECT 
                tts_office_config.*,
                countries_list.country_name,
                countries_list.`code` country_code,
                weekend_list.weekend_name
                from tts_office_config 
                INNER JOIN countries_list on tts_office_config.country_id=countries_list.id
                INNER JOIN weekend_list on tts_office_config.default_weekend_id=weekend_list.id
                where tts_office_config.`status`=1 ORDER BY tts_office_config.id DESC
            """
        )

        result = self.DB.execute(sqlQuery)
        resultData = result.fetchall()
        if resultData:
            return await self.fetchData(result, resultData)
        else:
            return False


    async def addNewOfficeInformation(self, data,objectData):

        sqlQuery = text(
            """
            INSERT INTO tts_office_config (`country_id`, `organization_name`, `address`, `main_responsible`, `director_name`, `finance_name`,`hr_name`, `office_email`, `office_mobile_number`, `default_langauge`, `office_start_date`, `default_timezone`, `default_work_start_time`, `default_work_end_time`, `default_weekend_id`, `default_office_ip`, `comments`, `created_id`, `user_ip` )
            VALUES (:country_id,:organization_name,:address,:main_responsible,:director_name,:finance_name,:hr_name,:office_email,:office_mobile_number,:default_langauge,:office_start_date,:default_timezone,:default_work_start_time,:default_work_end_time,:default_weekend_id,:default_office_ip,:comments,:created_id,:user_ip)
            """
        )
        #print(sqlQuery)

        result=  self.DB.execute(sqlQuery,
                                 {
                                     'country_id': data.country_id,
                                     'organization_name': data.organization_name,
                                     'address': data.address,
                                     'main_responsible': data.main_responsible,
                                     'director_name': data.director_name,
                                     'finance_name': data.finance_name,
                                     'hr_name': data.hr_name,
                                     'office_email': data.office_email,
                                     'office_mobile_number': data.office_mobile_number,
                                     'default_langauge': data.default_langauge,
                                     'office_start_date': data.office_start_date,
                                     'default_timezone': data.default_timezone,
                                     'default_work_start_time': data.default_work_start_time,
                                     'default_work_end_time': data.default_work_end_time,
                                     'default_weekend_id': data.default_weekend_id,
                                     'default_office_ip': data.default_office_ip,
                                     'comments': data.comments,
                                     'created_id': data.user_id,
                                     'user_ip': data.user_ip

                                 }
                                 )
        last_insert_id = result.lastrowid

       # data = result.fetchall()  # result.fetchall()
        if last_insert_id:
            return last_insert_id
        else:
            return False


    async def updateOfficeInformation(self, data):
        try:
            # self.DB.begin()

            sql_query = text(
                "UPDATE tts_office_config SET `country_id` = :country_id, `organization_name` = :organization_name, `address` = :address, `main_responsible` = :main_responsible, `director_name` = :director_name, `finance_name` = :finance_name, `hr_name` = :hr_name, `office_email` = :office_email, `office_mobile_number` = :office_mobile_number, `default_langauge` = :default_langauge, `office_start_date` = :office_start_date, `default_timezone` = :default_timezone, `default_work_start_time` = :default_work_start_time, `default_work_end_time` = :default_work_end_time, `default_weekend_id` = :default_weekend_id, `default_office_ip` = :default_office_ip, `comments` = :comments, `updated_id` = :updated_id, `user_ip` = :user_ip WHERE id = :office_id")


            result = self.DB.execute(sql_query, {

                'office_id': data.office_id,
            'country_id': data.country_id,
            'organization_name': data.organization_name,
            'address': data.address,
            'main_responsible': data.main_responsible,
            'director_name': data.director_name,
            'finance_name': data.finance_name,
            'hr_name': data.hr_name,
            'office_email': data.office_email,
            'office_mobile_number': data.office_mobile_number,
            'default_langauge': data.default_langauge,
            'office_start_date': data.office_start_date,
            'default_timezone': data.default_timezone,
            'default_work_start_time': data.default_work_start_time,
            'default_work_end_time': data.default_work_end_time,
            'default_weekend_id': data.default_weekend_id,
            'default_office_ip': data.default_office_ip,
            'comments': data.comments,
            'updated_id': data.user_id,
            'user_ip': data.user_ip


            })

            self.DB.commit()

            if result.rowcount > 0:
                return "success"
            else:
                return "failed"

        except IntegrityError as e:
            # self.DB.rollback()
            return "failed"
        except Exception as e:
            # self.DB.rollback()
            print(f"Error: {e}")
            return "error"

        finally:
            self.DB.close()


    async def userConfigAllList(self, data):

        sqlQuery = text(
            """
            SELECT 
                tts_user_config.*,
                users.first_name, users.last_name,users.email,users.mobile_number,users.username,
                weekend_list.weekend_name,
                tts_office_config.organization_name,tts_office_config.office_email,tts_office_config.default_langauge,tts_office_config.default_timezone,
                tts_office_config.default_weekend_id,tts_office_config.default_work_start_time,tts_office_config.default_work_end_time
                from tts_user_config
                INNER JOIN users on tts_user_config.user_id=users.id 
                INNER JOIN weekend_list on tts_user_config.weekend_id=weekend_list.id
                INNER JOIN tts_office_config on tts_user_config.office_id=tts_office_config.id
                ORDER BY tts_office_config.id DESC
            
            """
        )

        result = self.DB.execute(sqlQuery)

        resultData = result.fetchall()
        if resultData:
            return await self.fetchData(result, resultData)
        else:
            return False

    async def userConfigList(self, data):

        sqlQuery = text(
            """
            SELECT 
            tts_user_config.*,
            users.first_name, users.last_name,users.email,users.mobile_number,
            tts_office_config.organization_name,tts_office_config.office_email,tts_office_config.default_langauge,tts_office_config.default_timezone,
            tts_office_config.default_weekend_id,tts_office_config.default_work_start_time,tts_office_config.default_work_end_time
            from tts_user_config
            INNER JOIN users on tts_user_config.user_id=users.id 
            INNER JOIN tts_office_config on tts_user_config.office_id=tts_office_config.id
            where tts_user_config.`status`=1 and tts_user_config.user_id=:user_id
            """
        )

        result = self.DB.execute(sqlQuery, {"user_id": data.user_id})

        resultData = result.fetchall()
        if resultData:
            return await self.fetchData(result, resultData)
        else:
            return False


    async def addUserConfig(self, data,objectData):

        sqlQuery = text(
            """
            INSERT INTO tts_user_config (`office_id`,`user_id`,`country_id`,`time_zone`,`work_start_time`,`work_end_time`,`weekend_id`,`comments`,`created_id`, `user_ip` )
            VALUES (:office_id,:user_id,:country_id,:time_zone,:work_start_time,:work_end_time,:weekend_id,:comments,:created_id,:user_ip)
            """
        )

        result=  self.DB.execute(sqlQuery,
                                 {
                                     'office_id': data.office_id,
                                     'user_id': data.user_id,
                                     'country_id': data.country_id,
                                     'time_zone': data.time_zone,
                                     'work_start_time': data.work_start_time,
                                     'work_end_time': data.work_end_time,
                                     'weekend_id': data.weekend_id,
                                     'comments': data.comments,
                                     'created_id': data.created_id,
                                     'user_ip': data.user_ip

                                 }
                                 )
        last_insert_id = result.lastrowid

       # data = result.fetchall()  # result.fetchall()
        if last_insert_id:
            return last_insert_id
        else:
            return False

    async def getUserConfigInfoById(self, user_config_id):

        sqlQuery = text(
            """
            SELECT *  from tts_user_config where id=:user_config_id order by id desc limit 1
            """
        )

        result=  self.DB.execute(sqlQuery, {"user_config_id": user_config_id})
        resultData = result.fetchone()

       # data = result.fetchall()  # result.fetchall()
        if resultData:
            return self.JSON.getEncodeData(resultData)
        else:
            return False

    async def getUserConfigInfoByUserID(self, user_id):

        sqlQuery = text(
            """
            SELECT *  from tts_user_config where id=:user_id order by id desc limit 1
            """
        )

        result = self.DB.execute(sqlQuery, {"user_id": user_id})
        resultData = result.fetchone()

        # data = result.fetchall()  # result.fetchall()
        if resultData:
            return self.JSON.getEncodeData(resultData)
        else:
            return False

    async def updateUserConfig(self, data):
        try:
            # self.DB.begin()

            sql_query = text(
                "UPDATE tts_user_config SET `office_id` =:office_id,`user_id` = :user_id,`country_id` = :country_id,`time_zone` = :time_zone,`joining_date` =:joining_date,`work_start_time` =:work_start_time,`work_end_time` = :work_end_time,`weekend_id` = :weekend_id,`comments` = :comments,`updated_id` = :updated_id,`user_ip` = :user_ip  WHERE id = :user_config_id"
            )

            result = self.DB.execute(sql_query, {

                'user_config_id': data.user_config_id,
                'office_id': data.office_id,
                'user_id': data.user_id,
                'country_id': data.country_id,
                'time_zone': data.time_zone,
                'joining_date':data.joining_date,
                'work_start_time': data.work_start_time,
                'work_end_time': data.work_end_time,
                'weekend_id': data.weekend_id,
                'comments': data.comments,
                'updated_id': data.created_id,
                'user_ip': data.user_ip

            })

            self.DB.commit()

            if result.rowcount > 0:
                return "success"
            else:
                return "failed"

        except IntegrityError as e:
            # self.DB.rollback()
            return "failed"
        except Exception as e:
            # self.DB.rollback()
            #print(f"Error: {e}")
            return "error"

        finally:
            self.DB.close()



    async def holidayList(self, data):

        sqlQuery = text(
            """
             SELECT 
             tts_office_holiday_config.*,
             tts_office_config.default_timezone,
                tts_office_config.default_langauge,
                tts_office_config.default_weekend_id,
                tts_office_config.default_work_start_time,
                tts_office_config.default_work_end_time 
             from tts_office_holiday_config
             INNER JOIN tts_office_config on tts_office_holiday_config.office_id=tts_office_config.id
             where tts_office_holiday_config.`status`=1 and tts_office_holiday_config.office_id=:office_id
            """
        )

        result = self.DB.execute(sqlQuery, {"office_id": data.office_id})

        resultData = result.fetchall()
        if resultData:
            return await self.fetchData(result, resultData)
        else:
            return False

    async def isAlreadyExist(self, data):

        sqlQuery = text(
            """
             SELECT   * from tts_office_holiday_config 
             where `year`=:year_data and `month_id`=:month_id and `day_id`=:day_id and `office_id`=:office_id
            """
        )

        result = self.DB.execute(sqlQuery, {"office_id":data.office_id,"year_data": data.year,"month_id": data.month_id,"day_id": data.day_id})

        resultData = result.fetchall()
        if resultData:
            return await self.fetchData(result, resultData)
        else:
            return False


    async def addHolidayList(self, data,objectData):

        sqlQuery = text(
            """
            INSERT INTO tts_office_holiday_config (`office_id`,`day_id`,`month_id`,`year`,`comments`,`created_id`, `user_ip` )
            VALUES (:office_id,:day_id,:month_id,:year,:comments,:created_id,:user_ip)
            """
        )

        result=  self.DB.execute(sqlQuery,
                                 {
                                     'office_id': data.office_id,
                                     'day_id': data.day_id,
                                     'month_id': data.month_id,
                                     'year': data.year,
                                     'comments': data.comments,
                                     'created_id': data.user_id,
                                     'user_ip': data.user_ip

                                 }
                                 )
        last_insert_id = result.lastrowid

       # data = result.fetchall()  # result.fetchall()
        if last_insert_id:
            return last_insert_id
        else:
            return False

    async def holidayInfoById(self, office_holiday_config_id):

        sqlQuery = text(
            """
            SELECT *  from tts_office_holiday_config where id=:office_holiday_config_id order by id desc limit 1
            """
        )

        result=  self.DB.execute(sqlQuery, {"office_holiday_config_id": office_holiday_config_id})
        resultData = result.fetchone()

       # data = result.fetchall()  # result.fetchall()
        if resultData:
            return self.JSON.getEncodeData(resultData)
        else:
            return False


    async def updateHolidayList(self, data):
        try:
            # self.DB.begin()

            sql_query = text(
                "UPDATE tts_office_holiday_config SET `office_id` =:office_id,`day_id` =:day_id,`month_id` =:month_id,`year` =:year,`comments` =:comments,`status` =:status,`updated_id` =:updated_id,`user_ip` =:user_ip  WHERE id = :office_holiday_config_id"
            )

            result = self.DB.execute(sql_query, {

                'office_holiday_config_id': data.office_holiday_config_id,
                'office_id': data.office_id,
                'day_id': data.day_id,
                'month_id': data.month_id,
                'year': data.year,
                'comments': data.comments,
                'status': data.status,
                'updated_id': data.user_id,
                'user_ip': data.user_ip,


            })

            self.DB.commit()

            if result.rowcount > 0:
                return "success"
            else:
                return "failed"

        except IntegrityError as e:
            # self.DB.rollback()
            return "failed"
        except Exception as e:
            # self.DB.rollback()
            #print(f"Error: {e}")
            return "error"

        finally:
            self.DB.close()