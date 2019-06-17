import mysql.connector
from DBConnect import DBConnect

class DBActivity:

    def __init__(self):
        conn = DBConnect()
        conn.autocommit = False
        self.dbConn = conn.mydb.cursor(dictionary=True)
        self.mydb = conn.mydb



    def query(self, inputQuery):
        try:
            self.inputQuery = inputQuery
            self.dbConn.execute(self.inputQuery)
            myresult = self.dbConn.fetchall()
            myresultCnt = self.dbConn.rowcount
            return {"data": myresult, "count": myresultCnt}
        except mysql.connector.Error as err:
            return {"data": [], "count": -1, "error": format(err) }




    def insert(self, inputQuery, inputData):
        try:
            self.inputQuery = inputQuery
            self.inputData = inputData

            self.dbConn.execute(self.inputQuery, self.inputData)
            myresultCnt = self.dbConn.lastrowid
            return {"count": myresultCnt}
        except mysql.connector.Error as err:
            return {"count": -1, "error": format(err)}

    def update(self, updateQuery, updateData):
        try:
            self.updateQuery = updateQuery
            self.updateData = updateData
            self.dbConn.execute(self.updateQuery, self.updateData)
            myresultCnt = self.dbConn.rowcount
            return {"count": myresultCnt}
        except mysql.connector.Error as err:
            return {"count": -1, "error": format(err)}

    def transctionCommit(self):
        try:
            self.mydb.commit()
            return {"count": 1}
        except mysql.connector.Error as err:
            # reverting changes because of exception
            self.mydb.rollback()
            return {"count": -1, "error": format(err)}

    def transactRollback(self):
        self.mydb.rollback()


db = DBActivity()