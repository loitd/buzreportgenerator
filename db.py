import psycopg2

class DB:
    def __init__(self):
        self.conn = None
        self.cur = None

    def connectPostgres(self):
        print("Begin database postgres connection.")
        self.conn = psycopg2.connect(host="localhost", database="test", user="test", password="123456")
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT version()")
        db_version = self.cur.fetchone()
        print(db_version)
        print("Connect made successfully.")
        return True
    
    def getMegabankData(self):
        print("Begin get Megabank's data")
        try:
            self.cur.execute("SELECT * FROM TBL_TEST")
            rows = self.cur.fetchall()
            for row in rows:
                print(row)
            return rows
        except Exception as e:
            print(e)

    def __del__(self):
        if self.cur is not None:
            self.cur.close()
        if self.conn is not None:
            self.conn.close()


