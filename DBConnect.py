import mysql.connector
from constants import *

# Singleton Database connection creation
class DBConnect:
    mydb = ""
    def __new__(cls):
        if not hasattr(cls, 'instance') or not cls.instance:
            cls.instance = super().__new__(cls)
            print("new Database Connection is created!");
            cls.mydb = mysql.connector.connect(
                host=DBHOST,
                user=DBUSERNAME,
                passwd=DBPASSWORD,
                database=DBNAME,
                autocommit=False
            )

        return cls.instance
