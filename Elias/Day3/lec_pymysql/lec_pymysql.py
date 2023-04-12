import pymysql
from icecream import ic

ic.configureOutput(includeContext=True)

# SQL Tutorial
# https://www.w3schools.com/sql/default.asp

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

    # Execute Only
    def execute_only(self, sql, values=None):
        try:
            # 'select * from lg_autotest;'
            # 'select * from lg_autotest where name = "Elias";'
            if values is None:
                self.cursor.execute(sql)

            # age = 20
            # name = 'Hong'
            # sql = 'select * from elias where name = "Hong" age = 20;'

            # sql = f'select * from elias where age = {age};'
            # sql = 'select * from elias where age = ' + age + ';'

            # sql = 'select * from elias where name = ' + name + ' and  age = ' + age + ';' # ERROR!!!
            # sql = 'select * from elias where name = "' + name + '" and  age = ' + age + ';' # OK
            # sql = f'select * from elias where name = {name} and age = {age};' # ERROR!!!
            # sql = f'select * from elias where name = "{name}" and age = {age};' # OK

            # sql = 'select * from elias where name = %s and age = %s;' # 권장드림
            # values = [elias, age] or (elias, age)
            else:
                self.cursor.execute(sql, values)

        except Exception as e:
            print(e)


