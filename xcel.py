from openpyxl import Workbook, load_workbook
class XCel:
    def __init__(self):
        print("Opening excel file ...")
        self.wb = load_workbook("./data/blank.xlsx")
        self.ws = self.wb["Sheet1"]
        print("Excel file opened!")
    
    def __del__(self):
        self.wb.close()
    
    def detectBlank(self, col=1):
        i = 1
        while 1:
            if self.ws.cell(column=1, row=i).value is None:
                return i
                break
            else:
                i = i + 1

    def writeMegabank(self, datas, posX, posY):
        print("Begin write Megabank")
        oriPosX = posX
        oriPosY = posY
        for data in datas:
            print("Writing: ", data)
            for dat in data:
                self.ws.cell(column=posY, row=posX, value=dat)
                posY = posY + 1
            posX = posX + 1
            posY = oriPosY
        self.wb.save(filename="./data/blank1.xlsx")
        print("Write Megabank successfully")
        return True

# Write something
# ws.cell(column=2, row=3, value="ahihi")


