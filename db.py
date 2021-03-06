# import psycopg2
import cx_Oracle
import pyodbc

class DB:
    def __init__(self, config):
        self.conn = None
        self.cur = None
        self.config = config
        # CRM
        self.connCRM = None
        self.curCRM = None
        # SQLSERVER
        self.connSQL = None
        self.curSQL = None
        # SAT
        self.connSAT = None
        self.curSAT = None
        # REPORTER
        self.connRPT = None
        self.curRPT = None
    
    # Now connect to all kind of used database
    def connectSQLTopup(self):
        print("Begin database SQLServer connection")
        self.connSQL = pyodbc.connect(self.config['TNS_SQLSRV_TOPUP'])
        self.curSQL = self.connSQL.cursor()
        print("Connected to SQL Topup successfully!")

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
    
    def connectOracleSAT(self):
        print("Begin database Oracle SAT connection.")
        self.connSAT = cx_Oracle.connect(self.config['TNS_ORACLE_SAT'])
        self.curSAT = self.connSAT.cursor()
        print("Connected to Oracle SAT successfully!")
    
    def connectOracleRPT(self):
        print("Begin database Oracle SAT connection.")
        self.connRPT = cx_Oracle.connect(self.config['TNS_ORACLE_REPORTER'])
        self.curRPT = self.connRPT.cursor()
        print("Connected to Oracle SAT successfully!")

    # After connecting to databases, now get data for each service
    # -------------------------------------------------------------------------------------------
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
        # need to manipulate data before returned
        print("Get Oracle Megabank data successfully!")
        return rows
    
    def getOracleMegabankDataV2(self, fromdate, todate):
        print("Begin get Oracle Megabank data from {0} to {1}".format(fromdate, todate))
        self.curCRM.execute(self.config['ORACLE_MEGABANK_SQL_V2'].format(fromdate, todate))
        rows = self.curCRM.fetchall()
        print("Get Oracle Megabank data successfully with len={0}".format(len(rows)))
        return rows
    
    def getOracleMegabankDataV3(self, fromdate, todate):
        print("Begin get Oracle Megabank data from {0} to {1}".format(fromdate, todate))
        self.curRPT.execute(self.config['ORACLE_MEGABANK_SQL_V3'].format(fromdate, todate))
        rows = self.curRPT.fetchall()
        print("Get Oracle Megabank data successfully with len={0}".format(len(rows)))
        return rows
    
    def getOracleTopupData(self):
        print("Begin get Oracle Topup data")
        self.curCRM.execute(self.config['ORACLE_TOPUP_SQL'])
        rows = self.curCRM.fetchall()
        print("Get Oracle Topup data successfully!")
        return rows
    
    # Updated tov3
    def getOracleTopupDataV2(self, fromdate, todate):
        print("Begin get Oracle Topup data from {0} to {1}".format(fromdate, todate))
        self.curCRM.execute(self.config['ORACLE_TOPUP_SQL_V3'].format(fromdate, todate))
        rows = self.curCRM.fetchall()
        print("Get Oracle Topup data successfully with len={0}".format(len(rows)))
        return rows
    
    def getSQLTopupData(self):
        print("Begin get SQL Topup data")
        self.curSQL.execute(self.config['SQL_TOPUP_SQL'])
        rows = self.curSQL.fetchall()
        print("Get SQL Topup data successfully!")
        return rows
    # More about convert to date: https://www.mssqltips.com/sqlservertip/1145/date-and-time-conversions-using-sql-server/
    def getSQLTopupDataV2(self, fromdate, todate):
        print("Begin get SQL Topup data from {0} to {1}".format(fromdate, todate))
        self.curSQL.execute(self.config['SQL_TOPUP_SQL_V2'].format(fromdate, todate))
        rows = self.curSQL.fetchall()
        print("Get SQL Topup data successfully!")
        return rows
    
    def getOracleSATData(self):
        print("Begin get Oracle SAT data")
        self.curSAT.execute(self.config['ORACLE_SAT_SQL'])
        rows = self.curSAT.fetchall()
        print("Get Oracle SAT data successfully!")
        return rows
    
    # Updated tov3
    def getOracleSATDataV2(self,fromdate,todate):
        print("Begin get Oracle SAT data from {0} to {1}".format(fromdate, todate))
        self.curSAT.execute(self.config['ORACLE_SAT_SQL_V3'].format(fromdate, todate))
        rows = self.curSAT.fetchall()
        print("Get Oracle SAT data successfully with len={0}".format(len(rows)))
        return rows
    
    def getOracleMCData(self):
        print("Begin get Oracle MC data")
        self.curRPT.execute(self.config['ORACLE_MC_SQL'])
        rows = self.curRPT.fetchall()
        print("Get Oracle MC data successfully!")
        return rows
    
    # V2 Added fromdate and todate
    # MOVED TOV3
    def getOracleMCDataV2(self, fromdate, todate):
        print("Begin get Oracle MC data from {0} to {1}".format(fromdate, todate))
        self.curRPT.execute(self.config['ORACLE_MC_SQL_V3'].format(fromdate, todate))
        rows = self.curRPT.fetchall()
        print("Get Oracle MC data successfully with len={0}".format(len(rows)))
        return rows
    
    def getOracleMDData(self):
        print("Begin get Oracle MD data")
        self.curRPT.execute(self.config['ORACLE_MD_SQL'])
        rows = self.curRPT.fetchall()
        print("Get Oracle MD data successfully!")
        return rows
    
    # V2 Added fromdate and todate
    # mOVED TO V3
    def getOracleMDDataV2(self, fromdate, todate):
        print("Begin get Oracle MD data from {0} to {1}".format(fromdate, todate))
        self.curRPT.execute(self.config['ORACLE_MD_SQL_V3'].format(fromdate, todate))
        rows = self.curRPT.fetchall()
        print("Get Oracle MD data successfully with len={0}".format(len(rows)))
        return rows
    
    def getOracleFDData(self):
        print("Begin get Oracle FD data")
        self.curRPT.execute(self.config['ORACLE_FD_SQL'])
        rows = self.curRPT.fetchall()
        print("Get Oracle FD data successfully!")
        return rows
    
    # V2 Added fromdate and todate   
    # aDDEDV3
    def getOracleFDDataV2(self, fromdate, todate):
        print("Begin get Oracle FD data from {0} to {1}".format(fromdate, todate))
        self.curRPT.execute(self.config['ORACLE_FD_SQL_V3'].format(fromdate, todate))
        rows = self.curRPT.fetchall()
        print("Get Oracle FD data successfully with len={0}".format(len(rows)))
        return rows
    
    def getOracleVERIFYData(self):
        print("Begin get Oracle VERIFY data")
        self.curRPT.execute(self.config['ORACLE_VERIFY_SQL'])
        rows = self.curRPT.fetchall()
        print("Get Oracle VERIFY data successfully!")
        return rows
    
    # V2 Added fromdate and todate   
    def getOracleVERIFYDataV2(self, fromdate, todate):
        print("Begin get Oracle VERIFY data from {0} to {1}".format(fromdate, todate))
        self.curRPT.execute(self.config['ORACLE_VERIFY_SQL_V2'].format(fromdate, todate))
        rows = self.curRPT.fetchall()
        print("Get Oracle VERIFY data successfully with len={0}".format(len(rows)))
        return rows
    
    def getOracleTHSData(self):
        print("Begin get Oracle THS data")
        self.curRPT.execute(self.config['ORACLE_THS_SQL'])
        rows = self.curRPT.fetchall()
        print("Get Oracle THS data successfully!")
        return rows
    
    # V2 Added fromdate and todate   
    def getOracleTHSDataV2(self, fromdate, todate):
        print("Begin get Oracle THS data from {0} to {1}".format(fromdate, todate))
        self.curRPT.execute(self.config['ORACLE_THS_SQL_V2'].format(fromdate, todate, fromdate, todate))
        rows = self.curRPT.fetchall()
        print("Get Oracle THS data successfully with len={0}".format(len(rows)))
        return rows
    
    # V2 Added fromdate and todate   
    def getOracleVADataV2(self, fromdate, todate):
        print("Begin get Oracle VA data from {0} to {1}".format(fromdate, todate))
        self.curRPT.execute(self.config['ORACLE_VA_SQL_V2'].format(fromdate, todate, fromdate, todate))
        rows = self.curRPT.fetchall()
        print("Get Oracle VA data successfully with len={0}".format(len(rows)))
        return rows
    
    # V1 Added fromdate and todate   
    def getOracleMerchantData(self, fromdate, todate):
        print("Begin get Oracle MGB Merchant data from {0} to {1}".format(fromdate, todate))
        self.curRPT.execute(self.config['ORACLE_MGBMERCHANTS_SQL'].format(fromdate, todate))
        rows = self.curRPT.fetchall()
        print("Get Oracle MGB Merchant data successfully with len={0}".format(len(rows)))
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
        if self.curSQL is not None:
            self.curSQL.close()
        if self.connSQL is not None:
            self.connSQL.close()
        if self.curSAT is not None:
            self.curSAT.close()
        if self.connSAT is not None:
            self.connSAT.close()
        if self.curRPT is not None:
            self.curRPT.close()
        if self.connRPT is not None:
            self.connRPT.close()


