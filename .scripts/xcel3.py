import xlrd, xlutils.copy
rd = xlrd.open_workbook("./.data/SaleReportTemplate.xls")
wb = xlutils.copy.copy(rd)
sh = wb.get_sheet(0)
wb.save("./.data/datanew.xls")