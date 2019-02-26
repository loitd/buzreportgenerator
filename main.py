from db import DB
from xcel import XCel
db = DB()
xcel = XCel()

db.connectPostgres()
datas = db.getMegabankData()

xcel.writeMegabank(datas, 3, 1)