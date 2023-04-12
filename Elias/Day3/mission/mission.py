from lec_pymysql import Database
from openpyxl import load_workbook
from openpyxl import Workbook
from openpyxl.styles import Alignment, PatternFill
from openpyxl.styles.fonts import Font
from openpyxl.styles.borders import Border, Side

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
DB_NAME = 'elias' # 반드시 자신의 Table 사용

def put_data_to_db(excel_file_name):
    pass

# Task2
# DB의 public_bicycle의 테이블에서 특정 데이터를 뽑아서, 엑셀로 저장하기
# 2020이후에 서초구에 생성된 자전거 대여서 목록데이터
# sql = 'SELECT * FROM elias WHERE DATE(install_date) >= "2020-01-01" AND region = "서초구";'
# elias 대신에 자신의 테이블사용

# sql = 'SELECT * FROM elias WHERE DATE(install_date) >= %s AND region = %s;'
# from_date = "2020-01-01"
# region = "서초구"
# values = (from_date, region)
# execut(sql, values)

def get_data_from_db(from_date, region, output_file_name):
    pass