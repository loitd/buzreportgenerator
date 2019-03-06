__author__ = 'Admin'
import cx_Oracle
import time
import pyodbc
# for check mailserver
import email
import smtplib
from smtplib import SMTPException
from email.mime.text import MIMEText
from email.utils import formatdate

##GLOBAL VARIABLE FOR DB

#listOracle = ['DATA02','DATA06','DATA07','DATA11','RAC21','EPURSE1','EPURSE2','RAC22','RAC31','RAC32','RAC33','OFFICE','OFFICE1','OFFICE2']
listOracle = ['DATA06','DATA07','RAC21','RAC22','EPURSE1','EPURSE2','RAC31','RAC32','RAC33','DATA09']
#listOracle = ['DATA02','DATA06','DATA07','DATA11','RAC31','RAC32','RAC33']
listSqlsvr = ['192.168.1.121','192.168.1.133']
userid = 'R_MON'
passwd = 'r_mon$$$'
dbtype = 'SQL Server'
dbname = 'master'

##GLOBAL VARIABLE FOR ALERT, ALERT
name_file = "LOGDB" + time.strftime("%Y%m%d") + ".txt"
path_file = "E:\\Backup_All\\REPORT_AND_LOG\\" + name_file
alertid = 'CALLCENTER'
alertpasswd = 'CALLCENTER123'
alerttns = 'EPURSE'
alertreceiver = '0949311992'
alertemail ='loitd@vnptepay.com.vn'


with open (path_file,'a') as f:
    f.write("#################################################################################################################################################################\n")
    f.write("                   KIEM_TRA_CONNECT TAI THOI DIEM:" + time.strftime("%Y-%m-%d %H:%M:%S") + "\n")
f.close()

def writelog(infolog):
    with open (path_file,'a') as f:
        f.write(infolog + "\n")
    f.close()

def sendsms(alertlog, alertype):
    alertstr = alertid + "/" + alertpasswd + "@" + alerttns
    alertconn = cx_Oracle.connect(alertstr)
    alertcur = alertconn.cursor()
    alertcur.callproc('sp_0009_add_request_daodh',(alertlog, alertlog, alertreceiver, alertemail, alertype,'DBA_Alert'))
    alertcur.close()
    alertconn.close()

def checkDb(type):
#type 1: check sqlserver, type 2: check oracle,type 0: check all
    if type == 1:
        checkSqlsvr()
    if type == 2:
        checkOracle()
    if type == 0:
        checkSqlsvr()
        checkOracle()

def checkSqlsvr():
    # sql1 = "select count(*) as 'numofconnections' from sys.sysprocesses"
    sql1 = "select B.name as 'dbname' ,count(A.spid) as 'sessions' from sys.sysprocesses A right outer join sys.sysdatabases B on (A.dbid = B.dbid ) where B.dbid not in(1,2,3,4) group by B.name order by dbname"
    for list in listSqlsvr:
        conn_string = 'DRIVER={'+ dbtype +'};SERVER='+ list +';DATABASE='+ dbname + ';UID=' + userid + ';PWD=' + passwd
        try:

            #print conn_string
            conn = pyodbc.connect(conn_string)
            curs = conn.cursor()
            curs.execute(sql1)
            rows = curs.fetchall()
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
            error, = e.args
            log = list + ": Error" + format(e)
            writelog(log)
            sendsms(log,1)

def checkOracle():
    sql2 = "select INST_ID,count(*) from gv$session group by INST_ID"
    for list in listOracle:
        connString = userid + "/" + passwd + "@" + list
        try:
            connect = cx_Oracle.connect(connString)
            curs = connect.cursor()
            curs.execute(sql2)
            rows = curs.fetchall()
            curs.close()
            log = list + ":" + " Number of connection:" + str(rows)
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
    emailList = ["loitd@vnptepay.com.vn"]
    for emailID in emailList:
        #print "Sending email to", emailID
        FROM = "loitd@vnptepay.com.vn"
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
if __name__ == "__main__":
    main()