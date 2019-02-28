# import pyexcel_xlsxr as pxr
# import pyexcel_xlsxw as pxw
# import time
# p1 = time.time()
# print("Begin processing file at {0}".format(p1))
# data = pxr.get_data("./.data/datanew.xlsx")
# p2 = time.time()
# print("File read done at {0} and cost: {1}".format(p2, (p2-p1)))
# data = {"ahihi": [
#     [1,21,"abc"],
#     [3,23,"ab3"],
# ]}
# pxw.save_data("./.data/datanew1.xlsx", data)
# p3 = time.time()
# print("File saved at {0} and cost: {1}".format(p3, (p3-p2)))

import pyexcel_xlsx as px
data = px.get_data("./.data/datarawonly.xlsx")
px.save_data("./.data/datanew.xlsx", data)