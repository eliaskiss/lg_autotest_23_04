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
        try:
            # 연결이 안되어 있으면
            if self.conn is None:
                self.conn = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd,
                                            db=self.db, charset='utf8')
                # id, reg_datetime, name, age --> row[0], row[1], row[2], row[3] : List
                # self.cursor = self.conn.cursor()

                # id, reg_datetime, name, age --> row['id'], row['reg_datetime'], row['name'], row['age'] : Dictionary
                self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            print('DB is connected')
        except Exception as e:
            print(e)

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
    def execute_and_return_one(self, sql, values=None):
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
        print('DB is disconnected')

if __name__ == '__main__':
    # DB 연결
    db = Database('117.52.91.88', 'dbAdmin', '1111', 'lg_autotest')
    db.connect_db()

    # # 다른 DB 선택
    # sql = 'user mydb;'
    # db.execute_only(sql)

    # # DB에 새로운 데이터 삽입
    # for _ in range(10):
    #     sql = 'insert into elias (name, age) value(%s, %s);'
    #     values = ('Elias', 20)
    #     # db.execute_and_commit(sql, values)
    #     db.execute_only(sql, values)
    # db.commit_only()

    # # DB의 모든 데이터를 가져오기
    # sql = 'select * from elias;'
    # # sql = 'select name, age from elias;'
    # data_list = db.execute_and_return(sql)
    # for data in data_list:
    #     ic(data)

    # DB에서 특정 데이터 하나만 가져오기
    sql = 'select * from elias where name="Elias Kim" and age=20;'
    # sql = 'select count(*) as total_count from elias;'
    # sql = 'select count(*) from elias;'
    data = db.execute_and_return_one(sql)
    ic(data)









    # DB 연결해제
    db.disconnect_db()
























