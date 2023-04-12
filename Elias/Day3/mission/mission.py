from openpyxl import load_workbook
from openpyxl import Workbook
from openpyxl.styles import Alignment, PatternFill
from openpyxl.styles.fonts import Font
from openpyxl.styles.borders import Border, Side
from lec_pymysql import Database

# Create Table SQL
# table_name 지정필요!!!!
# CREATE TABLE `bicycle` (
#   `id` INT(11) NOT NULL AUTO_INCREMENT,
#   `reg_datetime` DATETIME DEFAULT CURRENT_TIMESTAMP(),
#   `station_number` INT(11) DEFAULT NULL,
#   `station_name` VARCHAR(128) DEFAULT NULL,
#   `region` VARCHAR(128) DEFAULT NULL,
#   `address` VARCHAR(1024) DEFAULT NULL,
#   `latitude` FLOAT DEFAULT NULL,
#   `longitude` FLOAT DEFAULT NULL,
#   `install_date` DATETIME DEFAULT NULL,
#   `lcd_count` INT(11) DEFAULT NULL,
#   `qr_count` INT(11) DEFAULT NULL,
#   `proc_type` VARCHAR(128) DEFAULT NULL,
#   KEY `id` (`id`)
# ) ENGINE=INNODB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

# Task1
# public_bicycle.xlsx 파일을 읽어서, DB의 public_bycycle의 테이블에 넣기

DB_URL = '117.52.91.88'
DB_USER = 'dbAdmin'
DB_PW = '1111'
DB_NAME = 'elias' # 반드시 자신의 DB 사용

db = Database(DB_URL, DB_USER, DB_PW, DB_NAME)
db.connect_db()
db.disconnect_db()

def put_data_to_db(excel_file_name):
    # Load wb from excel file
    wb = load_workbook(excel_file_name, data_only=True, read_only=True)

    # Select work sheet
    ws = wb.active
    # ws = wb['대여소현황']

    # DB 객체 생성
    db = Database(DB_URL, DB_USER, DB_PW, DB_NAME)

    # DB 연결
    db.connect_db()

    # Read data from work sheet
    for row in ws.iter_rows(min_row=6):
        station_number =  row[0].value
        station_name = row[1].value
        region = row[2].value
        address = row[3].value
        latitude = row[4].value
        longitude = row[5].value
        install_date = row[6].value
        lcd_count = row[7].value
        qr_count = row[8].value
        proc_type = row[9].value

        sql = 'insert into elias (station_number, station_name, region, address, latitude, longitude,' \
              'install_date, lcd_count, qr_count, proc_type) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
        values = (station_number, station_name, region, address, latitude, longitude,
                  install_date, lcd_count, qr_count, proc_type)

        db.execute_only(sql, values)
    db.commit_only()
    db.disconnect_db()

    # db.... # insert to db

    pass

# Task2
# DB의 bicycle의 테이블에서 특정 데이터를 뽑아서, 엑셀로 저장하기
# 2020이후에 서초구에 생성된 자전거 대여소 목록데이터
# sql = 'SELECT * FROM bicycle WHERE DATE(install_date) >= "2020-01-01" AND region = "서초구";'

# sql = 'SELECT * FROM elias WHERE DATE(install_date) >= %s AND region = %s;'
# from_date = "2020-01-01"
# region = "서초구"
# values = (from_date, region)
# execute(sql, values)

def get_data_from_db(from_date, region, output_file_name):
    # Create Workbook

    # Select Worksheet

    # Rename Worksheet

    # Header (Merge)

    # Get data from DB with sql = 'SELECT * FROM bicycle WHERE DATE(install_date) >= "2020-01-01" AND region = "서초구";'

    # for data in data_list:
    #   Add to worksheet

    # Add Styling
    pass

