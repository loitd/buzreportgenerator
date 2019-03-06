__author__ = 'Admin'
import cx_Oracle
import time, sys, os, datetime
import pyodbc
# for check mailserver
import email
import smtplib
from smtplib import SMTPException
from email.mime.text import MIMEText
from email.utils import formatdate
from serveralarm import ServerAlarm

##GLOBAL VARIABLE FOR DB

#listOracle = ['DATA02','DATA06','DATA07','DATA11','RAC21','EPURSE1','EPURSE2','RAC22','RAC31','RAC32','RAC33','OFFICE','OFFICE1','OFFICE2']
#listOracle = ['DATA02','DATA06','DATA07','RAC21','RAC22','EPURSE1','EPURSE2','RAC31','RAC32','RAC33','OFFICE','OFFICE1','OFFICE2','DATA09', 'DB12C_PDB5']
#listOracle = ['DATA02','DATA06','DATA07','DATA09','OFFICE1','OFFICE2','DB12C_PDB2','DB12C_PDB3','DB12C_PDB4','DB12C_PDB5','DG3','DG4']
listOracle = ['DG1','DG3','DG5','DG7','DG2','DG4','DG6','DG8']
#,'DG2','DG4','DG6','DG8'
#listOracle = ['DATA02','DG1','DG2','DG3','DG4','DG5','DG7']
#listSqlsvr = ['192.168.1.121','192.168.1.133','192.168.1.125','192.168.1.126']
listSqlsvr = ['192.168.1.125','192.168.1.126']
userid = 'R_MON'
passwd = 'r_mon$$$'
dbtype = 'SQL Server'
dbname = 'master'

##GLOBAL VARIABLE FOR ALERT, ALERT
name_file = "LOGDB" + time.strftime("%Y%m%d") + ".txt"
path_file = "E:\\Backup_All\\REPORT_AND_LOG\\" + name_file
alertid = 'CALLCENTER'
alertpasswd = 'CALLCENTER123'
alerttns = 'DG7'
alertreceiver = '0918612485;0919358413;0911458895'
#alertreceiver = '0911458895'
alertemail ='hethong@vnptepay.com.vn'


with open (path_file,'a') as f:
    f.write("#################################################################################################################################################################\n")
    f.write("                   KIEM_TRA_CONNECT TAI THOI DIEM:" + time.strftime("%Y-%m-%d %H:%M:%S") + "\n")
f.close()

def writelog(infolog):
    with open (path_file,'a') as f:
        f.write(infolog + "\n")
    f.close()

def sendsms(alertlog, alertype):
    #trim smssend to 200
    alertlog = alertlog[0:199]
    print("Begin sending SMS:" + alertlog)
    alertstr = alertid + "/" + alertpasswd + "@" + alerttns
    alertconn = cx_Oracle.connect(alertstr)
    alertcur = alertconn.cursor()
    alertcur.callproc('sp_0009_add_request_daodh',(alertlog, alertlog, alertreceiver, alertemail, alertype,'DBA_Alert'))
    alertcur.close()
    alertconn.close()

def sendsms2(alertlog, alertype, alertreceiver, alertemail):
    #trim smssend to 200
    alertlog = alertlog[0:199]
    print("Begin sending SMS:" + alertlog)
    alertstr = alertid + "/" + alertpasswd + "@" + alerttns
    alertconn = cx_Oracle.connect(alertstr)
    alertcur = alertconn.cursor()
    alertcur.callproc('sp_0009_add_request_daodh',(alertlog, alertlog, alertreceiver, alertemail, alertype,'DBA_Alert'))
    alertcur.close()
    alertconn.close()

def checkDb(type):
    print("Begin check type 1: check sqlserver, type 2: check oracle,type 0: check all")
    if type == 1:
        checkSqlsvr()
    if type == 2:
        checkOracle()
    if type == 0:
        checkSqlsvr()
        checkOracle()
        checkCTH()
        checkTopup()

def checkTopup():
    print("Begin checking service: Topup")
    sql1 = """WITH AA AS (SELECT CASE TRANS_STATUS WHEN '0' THEN 'S' WHEN '99' THEN 'P' ELSE 'F' END AS TSTATUS, 
SERVICE_PROVIDER_CODE AS SPC FROM TBL_TRANSACTIONS WHERE TRANS_DATE > SYSDATE - 1/(24*6))
SELECT (SELECT COUNT(*) FROM AA WHERE TSTATUS = 'S') AS SUC, 
(SELECT COUNT(*) FROM AA) AS TOT,
(SELECT COUNT(*) FROM AA WHERE TSTATUS ='S' AND SPC='VNP') AS SVNP, 
(SELECT COUNT(*) FROM AA WHERE SPC='VNP') AS TVNP,
(SELECT COUNT(*) FROM AA WHERE TSTATUS ='S' AND SPC='VMS') AS FVMS,
(SELECT COUNT(*) FROM AA WHERE SPC='VMS') AS TVMS,
(SELECT COUNT(*) FROM AA WHERE TSTATUS ='S' AND SPC='VTT') AS FVTT,
(SELECT COUNT(*) FROM AA WHERE SPC='VTT') AS TVTT,
(SELECT COUNT(*) FROM AA WHERE TSTATUS ='S' AND SPC='BEE') AS FBEE,
(SELECT COUNT(*) FROM AA WHERE SPC='BEE') AS TBEE,
(SELECT COUNT(*) FROM AA WHERE TSTATUS ='S' AND SPC='VNM') AS FVNM,
(SELECT COUNT(*) FROM AA WHERE SPC='VNM') AS TVNM
FROM DUAL"""
    connString = r"DIRECTTOPUP/DIRECTTOPUP123@DG6"
    try:
        connect = cx_Oracle.connect(connString)
        curs = connect.cursor()
        print("* Connected successfully [{0}]".format("DIRECTTOPUP"))			
        curs.execute(sql1)
        row1 = curs.fetchone()
        #TOPUP percentage of sucessfull trxin10 min
        #print(row1)
        if (row1):
            ratio = float(row1[0])/int(row1[1]) if int(row1[1]) else 0 
            ratiovnp = float(row1[2])/int(row1[3]) if int(row1[3]) else 0
            ratiovms = float(row1[4])/int(row1[5]) if int(row1[5]) else 0
            ratiovtt = float(row1[6])/int(row1[7]) if int(row1[7]) else 0
            ratiobee = float(row1[8])/int(row1[9]) if int(row1[9]) else 0
            ratiovnm = float(row1[10])/int(row1[11]) if int(row1[11]) else 0
            msg = "*TOPUP:{0:.2f}(S:{1}/T:{2})/RVNP:{3:.2f}(S:{4}/T:{5})/RVMS:{6:.2f}(S:{7}/T:{8})/RVTT:{9:.2f}(S:{10}/T:{11})/RBEE:{12:.2f}(S:{13}/T:{14})/RVNM:{15:.2f}(S:{16}/T:{17}) in last 10 min".format(ratio, row1[0], row1[1], ratiovnp, row1[2], row1[3], ratiovms, row1[4], row1[5], ratiovtt, row1[6], row1[7], ratiobee, row1[8], row1[9], ratiovnm, row1[10], row1[11])
            print('1st', msg)
            if (ratiovnp<0.5 and int(row1[3]>20)) or (ratiovms<0.5 and int(row1[5]>20)) or (ratiovtt<0.0 and int(row1[7]>5)) or (ratiobee<0.3 and int(row1[9]>5)) or (ratiovnm<0.3 and int(row1[11]>5)): #when ratio < 0.7 and total > 10
                #
                sendsms2(msg, 1, '0911458895,0919358413', 'loitd@vnptepay.com.vn')	
                #sendsms2(msg, 1, '0911458895', 'loitd@vnptepay.com.vn')	
                #pass
            else:
                #print('2nd',msg)
                pass
    except Exception as e:
        print(e)
		
def checkCTH():
    print("Begin checking service: CTH/CCH/FBK")
    sql1  = "SELECT COUNT(*) AS TOTAL FROM TBL_TRANSACTION WHERE (TRANS_TIME-TRANS_BEHALF_TIME)*24*60 >= 1 AND TRANS_TIME > SYSDATE - 1/(24*6)"
    sql11 = "SELECT COUNT(*) AS TOTAL FROM TBL_TRANSACTION WHERE (TRANS_TIME-TRANS_BEHALF_TIME)*24*60 >= 2 AND TRANS_TIME > SYSDATE - 1/(24*6)"	
    sql2 = "SELECT COUNT(*) AS TOTAL FROM TBL_MONEY_TRANSFER_TRANSACTION WHERE TRANS_TIME > SYSDATE - 1/24"
    sql3 = "SELECT ACC_NO, REQUEST_AMOUNT, ACC_NAME,COUNT(*) AS DUPNO FROM TBL_MONEY_TRANSFER_TRANSACTION WHERE TRANS_TIME > SYSDATE - 1/24 AND GW_STATUS_RESPONSE in ('99', '11', '07', '13', '00') GROUP BY ACC_NO, REQUEST_AMOUNT, ACC_NAME HAVING COUNT(*) > 1"
    sql4 = "WITH AA AS (SELECT * FROM CONGTHUHO.TBL_MONEY_TRANSFER_TRANSACTION WHERE TRANS_TIME > SYSDATE - 1/(24*6)) SELECT (SELECT COUNT(*) FROM AA WHERE AA.STATUS = 200) AS SUC, (SELECT COUNT(*) FROM AA) AS TOTAL, (SELECT COUNT(*) AS SUC FROM AA WHERE AA.STATUS = 200)/(SELECT COUNT(*) AS TOTAL FROM AA) AS PERCENTAGE FROM DUAL"
    sql5 = "SELECT COUNT(*) FROM (SELECT * FROM CONGTHUHO.TBL_MONEY_TRANSFER_TRANSACTION AA WHERE ROWNUM <= 5 ORDER BY AA.REQUEST_TIME DESC) BB WHERE BB.STATUS <> 200"
    connString = r"CONGTHUHO/CTH$@DG8"
    try:
        connect = cx_Oracle.connect(connString)
        curs = connect.cursor()
        print("* Connected successfully [{0}]".format("CONGTHUHO"))			
        curs.execute(sql1)
        rows = curs.fetchone()
        #
        curs.execute(sql11)
        row11 = curs.fetchone()
        #curs.close()
        curs.execute(sql2)
        row2 = curs.fetchone()
        #curs.close()

        curs.execute(sql3)
        row3 = curs.fetchone()
        #curs.close()

        curs.execute(sql4)
        row4 = curs.fetchone()
        #curs.close()
        curs.execute(sql5)
        row5 = curs.fetchone()
        curs.close()

        #CTH
        msg = "*[CTH] There're {0} trx above 1 min. {1} trx above 2 min/recent 10m.".format(int(rows[0]), int(row11[0]))		
        if (int(rows[0]) > 0):
            #msg = "* [CTH] There're {0} transactions above 1 min. {1} transactions above 2 min/10m".format(int(rows[0]), int(row11[0]))
            print(msg)
            sendsms2(msg, 1, '0911458895,0945274384,0976395263,0919358413', 'loitd@vnptepay.com.vn')	
        else:
            #msg = "* [CTH] Co {0} giao dich vuot nguong 1 phut".format(int(rows[0]))
            print(msg)		
        #FIRM
        if (int(row2[0]) == 0):
            msg = "*[FIRM] There're {0} trx in 60 min".format(int(row2[0]))
            print(msg)
            #sendsms2(msg, 1, '0911458895', 'loitd@vnptepay.com.vn')	
        else:
            msg = "*[FIRM] There're {0} trx in 60 min".format(int(row2[0]))
            print(msg)		
        #FIRM duplicate
        if (row3):
            msg = "*[FIRM] Duplicated trx on acc_no: {0} in last 60 min".format(row3[0])
            print(msg)
            if (datetime.datetime.now().minute == 0):
                sendsms2(msg, 1, '0911458895,0919358413', 'loitd@vnptepay.com.vn')	
        else:
            msg = "*[FIRM] No duplicated trx in last 60 min"
            print(msg)
        #FIRM percentage of sucessfull trxin10 min
        if (row4):
            msg = "*EPAYFIRM:Success ratio: {0:.2f} (S:{1}/T:{2}) in last 10 min".format(row4[2], row4[0], row4[1])
            print(msg)
            if (int(row4[2]<0.2) and int(row4[1]>20)): #when ratio < 0.7 and total > 10
                #
                sendsms2(msg, 1, '0911458895,0934688101,0919358413,0969570641,0379915154,0948150284,0965855530,0931108633,0354814809,0973570357', 'loitd@vnptepay.com.vn')	
                #sendsms2(msg, 1, '0911458895', 'loitd@vnptepay.com.vn')	
        else:
            msg = "*EPAYFIRM:Success ratio: {0:.1f} (S:{1}/T:{2}) in last 10 min".format(row4[2], row4[0], row4[1])
            print(msg)
        
        #FIRM last 5 fails in a row
        if (row5):
            msg = "*EPAYFIRM:No of failed/pending: {0:.2f} in a row of 5 trx".format(row5[0])
            print(msg)
            if (int(row5[0]) == 5): #when 5 failed in a row
                #
                sendsms2(msg, 1, '0911458895,0934688101,0919358413,0969570641,0379915154,0948150284,0965855530,0931108633,0354814809,0973570357', 'loitd@vnptepay.com.vn')	
                #sendsms2(msg, 1, '0911458895', 'loitd@vnptepay.com.vn')	
        else:
            msg = "*EPAYFIRM:No of failed/pending: {0:.2f} in a row of 5 trx".format(row5[0])
            print(msg)
    except Exception as e:
        print(e)


def checkSqlsvr():
    print("* Begin checking SQLSERVERs")
    # sql1 = "select count(*) as 'numofconnections' from sys.sysprocesses"
    sql1 = "select B.name as 'dbname' ,count(A.spid) as 'sessions' from sys.sysprocesses A right outer join sys.sysdatabases B on (A.dbid = B.dbid ) where B.dbid not in(1,2,3,4) group by B.name order by dbname"
    for list in listSqlsvr:
        print(list)
        conn_string = 'DRIVER={'+ dbtype +'};SERVER='+ list +';DATABASE='+ dbname + ';UID=' + userid + ';PWD=' + passwd
        try:
            #print conn_string
            conn = pyodbc.connect(conn_string)
            curs = conn.cursor()
            curs.execute(sql1)
            rows = curs.fetchall()
            # print(rows)
            # while True:
            #     rows = curs.fetchone()
            #     if not rows:
            #         break
            #     print rows.dbname, rows.sessions
            log = list + ":" + " Number of connection:" + str(rows)
            writelog(log)
            curs.close()
            conn.close()
        except pyodbc.DatabaseError as e:
            #error, = e.args
            log = list + ": Error" + format(e)
            writelog(log)
            sendsms(log,1)
        except pyodbc.Error as e:
            ecode,econtent = e
            log = list + ":Er:" + format(econtent)
            writelog(log)
            sendsms(log,1)
        except Exception as e:
            #error, = e.args
            log = list + ": Error" + format(e)
            writelog(log)
            sendsms(log,1)

def checkOracle():
    print("* Begin checking Oracles")
    sql2 = "select space_limit/1024000000 as slimit, space_used/1024000000 as sused, space_used*100/space_limit as spercent from v$recovery_file_dest"
    sql3 = "select value from v$dataguard_stats where name='apply lag'"
    for list in listOracle:
        print("Begin checking: " + list)
        connString = userid + "/" + passwd + "@" + list
        try:
            connect = cx_Oracle.connect(connString)
            curs = connect.cursor()
            print("* Connected successfully [{0}]".format(userid))			
            curs.execute(sql2)
            rows = curs.fetchone()
            curs.execute(sql3)					
            lags = curs.fetchone()
            curs.close()
            print("* Get space successfully: {0}".format(rows))
            if (int(rows[2]) > 50):
                log = list + ".FRA: {0}".format(rows[2])
                sendsms(log,1)				
                log = list + ".FRA: {0}".format(rows[2])
                writelog(log)
            print("* Get lags successfully: {0}".format(lags))
            #if (lags is not None and lags[0] not in ['+00 00:00:00','+00 00:00:01','+00 00:00:02','+00 00:00:03']):
            if (lags is not None and lags[0] not in ['+00 00:00:00','+00 00:00:01','+00 00:00:02','+00 00:00:03']):
                log = list + ".LAG: {0}".format(lags[0])
                sendsms(log,1)
                #print(lags)
                writelog(log)
            elif (lags is None and list in ['DG2', 'DG4', 'DG6', 'DG8']):
                log = list + ".LAG: {0}".format("Unable to get lags. Check asap!")
                sendsms(log,1)
                #print(lags)
                writelog(log)
            connect.close()
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            if error.code == 1017:
                log = list + ":" + " Please check out credentials."
                writelog(log)
            else:
                log = list + ": Error" + format(e)
                writelog(log)
                sendsms(log,1)

def checkMailserver():
    emailList = ["longtn@vnptepay.com.vn"]
    for emailID in emailList:
        #print "Sending email to", emailID
        FROM = "longtn@vnptepay.com.vn"
        TO = emailID
        message = "Mail server is online"
        msg = MIMEText(message, 'plain')
        msg["Subject"] = "Email check Mail server"
        msg["Message-id"] = email.Utils.make_msgid()
        msg["From"] = FROM
        msg["To"] = TO
        msg['Date'] = formatdate(localtime = True)
        host = "mail.vnptepay.com.vn"
        try:
            server = smtplib.SMTP(host)
        except smtplib.socket.gaierror:
            log = "Could not connect to mailsvr: " + host
            writelog(log)
            sendsms(log,1)
            return False
        try:
            server.sendmail(FROM, TO, msg.as_string())
            log = "Mail server online"
        except smtplib.SMTPException:
            log = "Unable to send mail via" + host
            print log
            sendsms(log,1)
        writelog(log)
        server.quit()

def main():
        checkDb(0)
        time.sleep(15)
if __name__ == "__main__":
    main()