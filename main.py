from db import DB
from xcel import XCel
import config
# All vars to store data
# Process Megabank data
megabankDatas, topupDatas, topupSQLDatas, satDatas, mcDatas, mdDatas, fdDatas, verifyDatas, thsDatas, vaDatas = (None,)*10
# topupSQLDatas = db.getSQLTopupData()

# Load config
config = config.loadConfig()
# Initialize database
db = DB(config)

def initDB():
    # Connect to dbs
    # db.connectPostgres()
    db.connectOracleCRM()
    db.connectSQLTopup()
    db.connectOracleSAT()
    db.connectOracleRPT()

def getAllDatas():
    # Process Megabank data
    megabankDatas = db.getOracleMegabankData()
    topupDatas = db.getOracleTopupData()
    topupSQLDatas = db.getSQLTopupData()
    satDatas = db.getOracleSATData()
    mcDatas = db.getOracleMCData()
    mdDatas = db.getOracleMDData()
    fdDatas = db.getOracleFDData()
    verifyDatas = db.getOracleVERIFYData()
    thsDatas = db.getOracleTHSData()

# Added fromdate and todate
def getAllDatasV2(fromdate, todate):
    # Using global
    global megabankDatas, topupDatas, topupSQLDatas, satDatas, mcDatas, mdDatas, fdDatas, verifyDatas, thsDatas, vaDatas
    # Process Megabank data
    megabankDatas = db.getOracleMegabankDataV3(fromdate, todate)
    topupDatas = db.getOracleTopupDataV2(fromdate, todate)
    topupSQLDatas = db.getSQLTopupDataV2(fromdate, todate)
    satDatas = db.getOracleSATDataV2(fromdate, todate)
    mcDatas = db.getOracleMCDataV2(fromdate, todate)
    mdDatas = db.getOracleMDDataV2(fromdate, todate)
    fdDatas = db.getOracleFDDataV2(fromdate, todate)
    verifyDatas = db.getOracleVERIFYDataV2(fromdate, todate)
    thsDatas = db.getOracleTHSDataV2(fromdate, todate)
    vaDatas = db.getOracleVADataV2(fromdate, todate)
    # print to test
    # print(megabankDatas)

def writeToExcel():
    # Using global
    global megabankDatas, topupDatas, topupSQLDatas, satDatas, mcDatas, mdDatas, fdDatas, verifyDatas, thsDatas, vaDatas
    # Init Xcel
    xcel = XCel(config)
    # Write Megabank to Xcel
    # megabankDatas = [('02/21/2019', 'Megabank', 'OTHERS', 394, 419923570, 'MB')]
    # topupDatas = [('02/21/2019', 'Topup', 'OTHERS', 394, 419923570, 'MB')]    
    xcel.appendMegabank(megabankDatas)
    xcel.appendTopup(topupDatas)
    xcel.appendSQLTopup(topupSQLDatas)
    xcel.appendSAT(satDatas)
    xcel.appendMC(mcDatas)
    xcel.appendMD(mdDatas)
    xcel.appendFD(fdDatas)
    xcel.appendVERIFY(verifyDatas)
    xcel.appendTHS(thsDatas)
    xcel.appendVA(vaDatas)
    # save workbook
    xcel.save()

# Write something
# ws.cell(column=2, row=3, value="ahihi")
if __name__ == "__main__":
    initDB()
    getAllDatasV2(20190304, 20190304)
    writeToExcel()