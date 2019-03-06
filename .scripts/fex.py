import csv
import cx_Oracle as cx_Oracle

def fexcoredetail(part):
	print('Trying connect to the db')
	sql = """select USERNAME,SESSIONID,PARTNER_CODE,TARGET_ACCOUNT ,SERVICE_PROVIDER_CODE,PROVIDER_SESSION,TRANS_STATUS,TRANSID,AMOUNT,TRANS_DATE,TRANSID_REQUEST,UPDATED_DATE, TELCO_STATUS,MESSAGE,UPDATED_CHECK_TIME,TRANS_STATUS_OLD, CREATED_DATE,TOPUP_TYPE,TELCO_TRANS_ID,SERVICE_PROVIDER_NAME, REC_ID,STATUS_UPDATE,STATUS_UPDATE_TIME from TBL_TRANSACTIONS partition ({0}) where TRANS_STATUS = 0""".format(part)

	outputfields = ['USERNAME', 'SESSIONID', 'PARTNER_CODE', 'TARGET_ACCOUNT', 'SERVICE_PROVIDER_CODE', 'PROVIDER_SESSION', 'TRANS_STATUS', 'TRANSID', 'AMOUNT', 'TRANS_DATE', 'TRANSID_REQUEST', 'UPDATED_DATE', 'TELCO_STATUS', 'MESSAGE', 'UPDATED_CHECK_TIME', 'TRANS_STATUS_OLD', 'CREATED_DATE', 'TOPUP_TYPE', 'TELCO_TRANS_ID', 'SERVICE_PROVIDER_NAME', 'REC_ID', 'STATUS_UPDATE', 'STATUS_UPDATE_TIME']
	tnsora = "HT_REPORT/123456@DG6"
	conn = cx_Oracle.connect(tnsora)
	cur = conn.cursor()
	print('Connected to the db')
	with open('E:/Dulieudauthang/fexcoredetail-{0}.csv'.format(part), 'wb+') as csvwfile:
		cwriter = csv.DictWriter(csvwfile, delimiter="@", fieldnames=outputfields)
		cwriter.writeheader()
		print('Done writing headers. Now executing sql')
		print(sql)
		cur.execute(sql)
		rows = cur.fetchall()
		print('Got data from db. Length: {0}'.format(len(rows)))
		if len(rows) > 0 and rows is not None:
			for row in rows:
				cwriter.writerow({	'USERNAME':row[0], 'SESSIONID':row[1], 'PARTNER_CODE': row[2],
									'TARGET_ACCOUNT': row[3], 'SERVICE_PROVIDER_CODE': row[4], 'PROVIDER_SESSION': row[5],
									'TRANS_STATUS': row[6], 'TRANSID': row[7], 'AMOUNT': row[8],
									'TRANS_DATE': row[9], 'TRANSID_REQUEST': row[10], 'UPDATED_DATE': row[11],
									'TELCO_STATUS': row[12], 'MESSAGE': row[13], 'UPDATED_CHECK_TIME': row[14],
									'TRANS_STATUS_OLD': row[15], 'CREATED_DATE': row[16], 'TOPUP_TYPE': row[17],
									'TELCO_TRANS_ID': row[18], 'SERVICE_PROVIDER_NAME': row[19], 'REC_ID': row[20],
									'STATUS_UPDATE': row[21], 'STATUS_UPDATE_TIME': row[22]
								})
				print('Done writing {0}'.format(row[0]))
			print('Done all writing.')

def fexconvdetail(begin, end):
	print('Trying connect to the db')
	sql = """SELECT QUEUE_ID, TRANS_ID, TRIM(TO_CHAR(TARGET_ACCOUNT, '99999999999999')) as TARGET_ACCOUNT, AMOUNT, STATUS, REQUEST_TIME, SVPROVIDER_CODE
	FROM ITOPUP_DIRECTGW.TBL_QUEUEU_ITOPUP_LOG WHERE STATUS IN ('0', '00') AND REQUEST_TIME BETWEEN TO_DATE ('{0}01 00:00:00', 'YYYYMMDD HH24:MI:SS') AND TO_DATE ('{1}01 00:00:00','YYYYMMDD HH24:MI:SS')
	UNION ALL
	SELECT QUEUE_ID, TRANS_ID, TARGET_ACCOUNT, AMOUNT, STATUS, REQUEST_TIME, SVPROVIDER_CODE
	FROM ITOPUP_DIRECTGW.TBL_QUEUEU_ITOPUP WHERE STATUS IN ('0', '00') AND REQUEST_TIME BETWEEN TO_DATE ('{2}01 00:00:00', 'YYYYMMDD HH24:MI:SS') AND TO_DATE ('{3}01 00:00:00','YYYYMMDD HH24:MI:SS')""".format(begin, end, begin, end)
  
	outputfields = ['QUEUE_ID', 'TRANS_ID', 'TARGET_ACCOUNT', 'AMOUNT', 'STATUS', 'REQUEST_TIME', 'SVPROVIDER_CODE']
	tnsora = "HT_REPORT/123456@DG6"
	conn = cx_Oracle.connect(tnsora)
	cur = conn.cursor()
	print('Connected to the db')
	with open('E:/Dulieudauthang/fexconvdetail-{0}.csv'.format(begin), 'wb+') as csvwfile:
		cwriter = csv.DictWriter(csvwfile, fieldnames=outputfields)
		cwriter.writeheader()
		print('Done writing headers. Now executing sql')
		cur.execute(sql)
		rows = cur.fetchall()
		print('Got data from db. Length: {0}'.format(len(rows)))
		if len(rows) > 0 and rows is not None:
			for row in rows:
				cwriter.writerow({	'QUEUE_ID':row[0], 'TRANS_ID':row[1], 'TARGET_ACCOUNT': row[2],
									'AMOUNT': row[3], 'STATUS': row[4], 'REQUEST_TIME': row[5],
									'SVPROVIDER_CODE': row[6]
								})
				print('Done writing {0}'.format(row[0]))
			print('Done all writing.')

def fexcoresum(begin, end):
	print('Trying connect to the db')
	sql = """SELECT PARTNER_CODE, SERVICE_PROVIDER_CODE,SERVICE_PROVIDER_NAME, AMOUNT,  
	to_char(TRANS_DATE, 'yyyymmdd') as TRANSDATE, 
	SUM(AMOUNT) as SUMAMOUNT, 
	count(*) as COUNTSAO
	FROM TBL_TRANSACTIONS partition(P{0}) WHERE trans_status = 0
    and to_char(TRANS_DATE, 'yyyymmdd') >= '{1}01'
    and to_char(TRANS_DATE, 'yyyymmdd') < '{2}01'
	GROUP BY PARTNER_CODE, SERVICE_PROVIDER_CODE,SERVICE_PROVIDER_NAME, to_char(TRANS_DATE, 'yyyymmdd'), AMOUNT
	ORDER BY PARTNER_CODE, SERVICE_PROVIDER_CODE,SERVICE_PROVIDER_NAME, to_char(TRANS_DATE, 'yyyymmdd'), AMOUNT""".format(begin, begin, end)
  
	outputfields = ['PARTNER_CODE', 'SERVICE_PROVIDER_CODE', 'SERVICE_PROVIDER_NAME', 'AMOUNT', 'TRANSDATE', 'SUMAMOUNT', 'COUNTSAO']
	tnsora = "HT_REPORT/123456@DG6"
	conn = cx_Oracle.connect(tnsora)
	cur = conn.cursor()
	print('Connected to the db')
	with open('E:/Dulieudauthang/fexcoresum-{0}.csv'.format(begin), 'wb+') as csvwfile:
		cwriter = csv.DictWriter(csvwfile, fieldnames=outputfields)
		cwriter.writeheader()
		print('Done writing headers. Now executing sql')
		print(sql)
		cur.execute(sql)
		rows = cur.fetchall()
		print('Got data from db. Length: {0}'.format(len(rows)))
		if len(rows) > 0 and rows is not None:
			for row in rows:
				cwriter.writerow({	'PARTNER_CODE':row[0], 'SERVICE_PROVIDER_CODE':row[1], 'SERVICE_PROVIDER_NAME': row[2],
									'AMOUNT': row[3], 'TRANSDATE': row[4], 'SUMAMOUNT': row[5],
									'COUNTSAO': row[6]
								})
				print('Done writing {0}'.format(row[0]))
			print('Done all writing.')

def fexconvsum(begin, end):
	print('Trying connect to the db')
	sql = """SELECT T.USERNAME, T.AMOUNT,T.SVPROVIDER_CODE, SUM (T.SOLUONG) as SSOLUONG, sum(T.SOLUONG*T.AMOUNT) as TOTAL
    FROM (  SELECT USERNAME, AMOUNT, SVPROVIDER_CODE,  COUNT (*) "SOLUONG"
              FROM ITOPUP_DIRECTGW.TBL_QUEUEU_ITOPUP_LOG PARTITION (P{0})
             WHERE STATUS IN ('0', '00')
          GROUP BY USERNAME, AMOUNT,SVPROVIDER_CODE
          UNION ALL
            SELECT USERNAME, AMOUNT, SVPROVIDER_CODE,COUNT (*) "SOLUONG"
              FROM ITOPUP_DIRECTGW.TBL_QUEUEU_ITOPUP
             WHERE     STATUS IN ('0', '00')
                   AND REQUEST_TIME BETWEEN TO_DATE ('{1}01 00:00:00',
                                                     'YYYYMMDD HH24:MI:SS')
                                        AND TO_DATE ('{2}01 00:00:00',
                                                     'YYYYMMDD HH24:MI:SS')
          GROUP BY USERNAME, AMOUNT,SVPROVIDER_CODE) T
	GROUP BY T.USERNAME, T.AMOUNT,T.SVPROVIDER_CODE
	ORDER BY T.USERNAME, T.AMOUNT, T.SVPROVIDER_CODE ASC""".format(begin, begin, end)
  
	outputfields = ['USERNAME', 'AMOUNT', 'SVPROVIDER_CODE', 'SSOLUONG', 'TOTAL']
	tnsora = "HT_REPORT/123456@DG6"
	conn = cx_Oracle.connect(tnsora)
	cur = conn.cursor()
	print('Connected to the db')
	with open('E:/Dulieudauthang/fexconvsum-{0}.csv'.format(begin), 'wb+') as csvwfile:
		cwriter = csv.DictWriter(csvwfile, fieldnames=outputfields)
		cwriter.writeheader()
		print('Done writing headers. Now executing sql')
		print(sql)
		cur.execute(sql)
		rows = cur.fetchall()
		print('Got data from db. Length: {0}'.format(len(rows)))
		if len(rows) > 0 and rows is not None:
			for row in rows:
				cwriter.writerow({	'USERNAME':row[0], 'AMOUNT':row[1], 'SVPROVIDER_CODE': row[2],
									'SSOLUONG': row[3], 'TOTAL': row[4]
								})
				print('Done writing {0}'.format(row[0]))
			print('Done all writing.')

if __name__ == '__main__':
	fexcoredetail('P201810')
	fexconvdetail('201810','201811')
	fexcoresum('201810','201811')
	fexconvsum('201810','201811')
	