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

    # Excute and Commit
    def execute_and_commit(self, sql, values=None):
        try:
            self.execute_only(sql, values)
            self.conn.commit()
        except Exception as e:
            print(e)

    # Commit Only
    def commit_only(self):
        try:
            self.conn.commit()
        except Exception as e:
            print(e)


    # Execute and Return All
    def execute_and_return(self, sql, values=None):
        try:
            self.execute_only(sql, values)
            data_list = self.cursor.fetchall()

            # 데이터가 없으면, None을 return하지않고, 빈 리스트를 return []
            if data_list is None:
                data_list = []

            return data_list
        except Exception as e:
            print(e)

    # Execute and Return One
    def execute_and_return_one(self, sql, values):
        try:
            self.execute_only(sql, values)
            data = self.cursor.fetchone()
            return data
        except Exception as e:
            print(e)

    # Close Connection
    def disconnect_db(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None
            self.cursor = None
























