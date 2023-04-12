import pymysql
from icecream import ic

ic.configureOutput(includeContext=True)

class Database:
    def __init__(self, host, user, passwd, db):
        self.host = host        # DB IP
        self.user = user        # Account
        self.passwd = passwd    # Password
        self.db = db            # Database Name

        self.conn = None        # DB Connection Object
        self.cursor = None      # DB Cursor Object

    def connect_db(self):
        # 연결이 안되어 있으면
        if self.conn is None:
            self.conn = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd,
                                        db=self.db, charset='utf8')
            # id, reg_datetime, name, age --> row[0], row[1], row[2], row[3] : List
            # self.cursor = self.conn.cursor()

            # id, reg_datetime, name, age --> row['id'], row['reg_datetime'], row['name'], row['age'] : Dictionary
            self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)

