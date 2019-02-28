from openpyxl import Workbook, load_workbook
import time
class XCel:
    def __init__(self, config):
        p1 = time.time()
        self.config = config
        print("Opening template file: {0}".format(self.config['SALE_REPORT_TEMPLATE']))
        self.wb = load_workbook(self.config['SALE_REPORT_TEMPLATE'], keep_vba=True)
        self.ws = self.wb[self.config['SHEET_DATA_RAW']]
        p2 = time.time()
        print("[{0}] Excel file opened!".format(p2-p1))
    
    def __del__(self):
        self.wb.close()
    
    def save(self, filename="./.data/new.xls"):
        self.wb.save(filename=filename)
    
    def detectBlank(self, col=1):
        i = 1
        while 1:
            if self.ws.cell(column=1, row=i).value is None:
                return i
                break
            else:
                i = i + 1

    def appendNext(self, datas, col):
        p1 = time.time()
        print("Begin appendNext with firstCol={0}".format(col))
        row = self.detectBlank(col=col)
        oriCol = col
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

# Write something
# ws.cell(column=2, row=3, value="ahihi")


