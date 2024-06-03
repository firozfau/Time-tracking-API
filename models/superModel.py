#eventModel.py
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text
from dbConnection.dbcon import SessionLocal
from libraries.jsonFormate import JsonFormate
from libraries.frz import  Frz
from libraries.evement_management import EventManagement
class SuperModel:
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
    async def eventNameList(self, data):

        sqlQuery = text(
            """
            SELECT *  from event_name_list where status=1 order by sort_index ASC
            """
        )

        result = self.DB.execute(sqlQuery)
        resultData = result.fetchall()
        if resultData:
            return await self.fetchData(result, resultData)
        else:
            return False
