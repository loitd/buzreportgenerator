from db import DB
from xcel import XCel
import config
# All vars to store data
# Process Megabank data
megabankDatas, topupDatas, satDatas, mcDatas, mdDatas, fdDatas, verifyDatas, thsDatas = (None,)*8
# topupSQLDatas = db.getSQLTopupData()

# Load config
config = config.loadConfig()
# Initialize database
db = DB(config)

def initAll():
    # Connect to dbs
    # db.connectPostgres()
    db.connectOracleCRM()
    # db.connectSQLTopup()
    db.connectOracleSAT()
    db.connectOracleRPT()

def getAllDatas():
    # Process Megabank data
    megabankDatas = db.getOracleMegabankData()
    topupDatas = db.getOracleTopupData()
    # topupSQLDatas = db.getSQLTopupData()
    satDatas = db.getOracleSATData()
    mcDatas = db.getOracleMCData()
    mdDatas = db.getOracleMDData()
    fdDatas = db.getOracleFDData()
    verifyDatas = db.getOracleVERIFYData()
    thsDatas = db.getOracleTHSData()

# Added fromdate and todate
def getAllDatasV2(fromdate, todate):
    # Using global
    global megabankDatas, topupDatas, satDatas, mcDatas, mdDatas, fdDatas, verifyDatas, thsDatas
    # Process Megabank data
    megabankDatas = db.getOracleMegabankDataV2(fromdate, todate)
    topupDatas = db.getOracleTopupDataV2(fromdate, todate)
    # topupSQLDatas = db.getSQLTopupData()
    satDatas = db.getOracleSATDataV2(fromdate, todate)
    mcDatas = db.getOracleMCDataV2(fromdate, todate)
    mdDatas = db.getOracleMDDataV2(fromdate, todate)
    fdDatas = db.getOracleFDDataV2(fromdate, todate)
    verifyDatas = db.getOracleVERIFYDataV2(fromdate, todate)
    thsDatas = db.getOracleTHSDataV2(fromdate, todate)
    # print to test
    # print(megabankDatas)

def writeToExcel():
    # Using global
    global megabankDatas, topupDatas, satDatas, mcDatas, mdDatas, fdDatas, verifyDatas, thsDatas
    # Init Xcel
    xcel = XCel(config)
    # Write Megabank to Xcel
    # megabankDatas = [('02/21/2019', 'Megabank', 'OTHERS', 394, 419923570, 'MB')]
    # topupDatas = [('02/21/2019', 'Topup', 'OTHERS', 394, 419923570, 'MB')]
    xcel.appendMegabank(megabankDatas)
    xcel.appendTopup(topupDatas)
    # xcel.appendSQLTopup(topupSQLDatas)
    xcel.appendSAT(satDatas)
    xcel.appendMC(mcDatas)
    xcel.appendMD(mdDatas)
    xcel.appendFD(fdDatas)
    xcel.appendVERIFY(verifyDatas)
    xcel.appendTHS(thsDatas)
    # save workbook
    xcel.save()

# Write something
# ws.cell(column=2, row=3, value="ahihi")
if __name__ == "__main__":
    initAll()
    getAllDatasV2(20190101, 20190302)
    writeToExcel()