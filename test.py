from xcel import XCel
import config
import datetime

# Load config
config = config.loadConfig(filename="./.config/test.config.json")

def writeToExcel():
    # Init Xcel
    xcel = XCel(config)
    # Write Megabank to Xcel
    megabankDatas = [('02/21/2019', 'Megabank', 'OTHERS', 394, 419923570, 'MB')]
    topupDatas = [(datetime.datetime.strptime('02/21/2019',"%m/%d/%Y"), 'Topup', 'OTHERS', 394, 419923570, 'MB')]    
    xcel.appendMegabank(megabankDatas)
    xcel.appendMegabank(topupDatas)
    # 
    xcel.save()

if __name__ == "__main__":
    writeToExcel()