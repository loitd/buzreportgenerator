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

# Process Megabank data
megabankDatas = db.getOracleMegabankData()
topupDatas = db.getOracleTopupData()
# Init Xcel
xcel = XCel(config)
# Write Megabank to Xcel
# datas = [('02/21/2019', 'Megabank', 'OTHERS', 394, 419923570, 'MB')]
xcel.appendMegabank(megabankDatas)
xcel.appendTopup(topupDatas)
# save workbook
xcel.save()