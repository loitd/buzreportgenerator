from openpyxl import Workbook, load_workbook
from halo import Halo
import time
class XCel:
    def __init__(self, config):
        p1 = time.time()
        self.config = config
        spin = Halo(text="Opening template file: {0}".format(self.config['SALE_REPORT_TEMPLATE']), spinner='dots')
        spin.start()
        self.wb = load_workbook(self.config['SALE_REPORT_TEMPLATE'], keep_vba=True)
        self.ws = self.wb[self.config['SHEET_DATA_RAW']]
        p2 = time.time()
        spin.stop()
        print("[{0}] Excel file opened!".format(p2-p1))
    
    def __del__(self):
        self.wb.close()
    
    def save(self, filename="./.data/new.xls"):
        p1 = time.time()
        spin = Halo(text="Begin saving file to: {0}".format(filename), spinner = 'dots')
        spin.start()
        self.wb.save(filename=filename)
        p2 = time.time()
        spin.stop()
        print("[{0}] Excel file saved!".format(p2-p1))
    
    def detectBlank(self, col=1):
        i = 1
        while 1:
            if self.ws.cell(column=col, row=i).value is None:
                return i
                break
            else:
                i = i + 1

    # Begin appending datas into first blank cell of the col
    def appendNext(self, datas, col):
        p1 = time.time()
        print("Begin appendNext with firstCol={0}".format(col))
        # First, detect for first bank row
        row = self.detectBlank(col=col)
        oriCol = col
        # Now writting 
        for data in datas:
            print("Writing: {0} at row/col: {1}/{2}".format(data, row, col))
            for dat in data:
                self.ws.cell(column=col, row=row, value=dat)
                col = col + 1
            row = row + 1
            col = oriCol
        p2 = time.time()
        print("[{0}] appendNext complete successfully".format(p2-p1))
        return True
    
    def appendMegabank(self, datas):
        print("Begin append data for Megabank")
        return self.appendNext(datas, col=1)
    
    def appendTopup(self, datas):
        print("Begin append data for Topup")
        return self.appendNext(datas, col=16)
    
    def appendSQLTopup(self, datas):
        print("Begin append data for SQL Topup")
        return self.appendNext(datas, col=16)
    
    def appendSAT(self, datas):
        print("Begin append data for SAT")
        return self.appendNext(datas, col=24)
    
    def appendMC(self, datas):
        print("Begin append data for MC")
        return self.appendNext(datas, col=51)
    
    def appendMD(self, datas):
        print("Begin append data for MD")
        return self.appendNext(datas, col=67)
    
    def appendFD(self, datas):
        print("Begin append data for FD")
        return self.appendNext(datas, col=75)
    
    def appendVERIFY(self, datas):
        print("Begin append data for VERIFY")
        return self.appendNext(datas, col=82)
    
    def appendTHS(self, datas):
        print("Begin append data for THS")
        return self.appendNext(datas, col=88)

# Write something
# ws.cell(column=2, row=3, value="ahihi")
if __name__ == "__main__":
    pass

