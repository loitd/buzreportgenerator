# This is processing excel files with pandas
import pandas as pd
print("Read all sheets in excel file")
dfs = pd.read_excel('./.data/SaleReportTemplate.xlsx', sheet_name='Dashboard')
print(dfs)
# Pandas writes Excel files using the Xlwt module for xls files and the Openpyxl or XlsxWriter modules for xlsx files.
print("Create a Pandas Excel writer using XlsxWriter as the engine.")
wr = pd.ExcelWriter('./.data/pd.xlsx', engine='xlsxwriter')
print("Convert the dataframe to an XlsxWriter Excel object.")
# for sheetName in dfs.keys():
#     dfs[sheetName].to_excel(wr, sheet_name=sheetName, index=False)
#     print("Wrote one sheet: {0}".format(sheetName))
##
# dfs.to_excel(wr, sheet_name='Data raw', startcol=3, startrow=6, header=False, index=False)
dfs.to_excel(wr, sheet_name='Data raw', header=False, index=False)
print("Close the Pandas Excel writer and output the Excel file.")
wr.save()

