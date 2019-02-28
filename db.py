# import psycopg2
import cx_Oracle

class DB:
    def __init__(self, config):
        self.conn = None
        self.cur = None
        self.config = config
        self.connCRM = None
        self.curCRM = None

    def connectPostgres(self):
        print("Begin database postgres connection.")
        self.conn = psycopg2.connect(host="localhost", database="test", user="test", password="123456")
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT version()")
        db_version = self.cur.fetchone()
        print(db_version)
        print("Connect made successfully.")
        return True
    
    def connectOracleCRM(self):
        print("Begin database Oracle CRM connection.")
        self.connCRM = cx_Oracle.connect(self.config['TNS_ORACLE_CRM'])
        self.curCRM = self.connCRM.cursor()
        print("Connected to Oracle CRM successfully!")

    
    def getPostgresMegabankData(self):
        print("Begin get Megabank's data")
        try:
            self.cur.execute("SELECT * FROM TBL_TEST")
            rows = self.cur.fetchall()
            for row in rows:
                print(row)
            return rows
        except Exception as e:
            print(e)
    
    def getOracleMegabankData(self):
        print("Begin get Oracle Megabank data")
        self.curCRM.execute(self.config['ORACLE_MEGABANK_SQL'])
        rows = self.curCRM.fetchall()
        print("Get Oracle Megabank data successfully!")
        return rows
    
    def getOracleTopupData(self):
        print("Begin get Oracle Topup data")
        self.curCRM.execute(self.config['ORACLE_TOPUP_SQL'])
        rows = self.curCRM.fetchall()
        print("Get Oracle Topup data successfully!")
        return rows

    def __del__(self):
        if self.cur is not None:
            self.cur.close()
        if self.conn is not None:
            self.conn.close()
        if self.curCRM is not None:
            self.curCRM.close()
        if self.connCRM is not None:
            self.connCRM.close()


