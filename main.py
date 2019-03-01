from db import DB
from xcel import XCel
import config
# Load config
config = config.loadConfig()
# Initialize database
db = DB(config)

# Connect to dbs
# db.connectPostgres()
db.connectOracleCRM()
# db.connectSQLTopup()
db.connectOracleSAT()
db.connectOracleRPT()

# Process Megabank data
megabankDatas = db.getOracleMegabankData()
topupDatas = db.getOracleTopupData()
# topupSQLDatas = db.getSQLTopupData()
satDatas = db.getOracleSATData()
mcDatas = db.getOracleMCData()
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
# save workbook
xcel.save()