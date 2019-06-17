import mysql.connector as mysqlDB
import sys
import DBActivity
from constants import *
from datetime import datetime
from datetime import timedelta

#Validating Date format
def validate(date_text):
    try:
        if date_text != datetime.strptime(date_text, DATEFORMAT).strftime(DATEFORMAT):
            raise ValueError
        elif datetime.strptime(date_text, DATEFORMAT) < datetime.now():
            raise ValueError
        return True
    except ValueError:
        return False

#Validating Date format
def validateList(key, listData):
    try:
        if key in listData:
            return True
    except:
        return False

#Validating Integer
def validateInteger(input):
    try:
        input = int(input)
        return True
    except:
        return False
