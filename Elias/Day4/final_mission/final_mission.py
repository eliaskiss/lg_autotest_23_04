# Task 1
# 기존에 만든 mission.py파일을 구동시킨 상태에서
# putty가 했던 동작(Power On/Off/GetStatus)을 윈도우 프로그래밍으로 전환
# pyinstaller mission.py -> tv_monitor.exe

# Task 2
# Excel -> DB
# DB -> Excel
# file_name, _ = QFileDialog.getOpenFileName(self, 'Open file', './')

# pip install pyqt5

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QThread, pyqtSlot, pyqtSignal

import logging
from datetime import datetime
import os
import sys

# Excel Modules
from openpyxl import load_workbook
from openpyxl import Workbook
from openpyxl.styles import Alignment, PatternFill
from openpyxl.styles.fonts import Font
from openpyxl.styles.borders import Border, Side

# Our modules
sys.path.append('../../Day3/lec_pymysql')
sys.path.append('../../Day1/lec_pyserial')

from lec_pymysql import Database
from lec_pyserial_class import MySerial

# UI 파일 포함하기
from main_ui import Ui_Dialog as Main_Ui

DISPLAY_LOG_IN_TERMNINAL = True

logger = logging.getLogger('MyLogger')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s (%(funcName)20s:%(lineno)4d) [%(levelname)s]: %(message)s')

# Print in terminal
if DISPLAY_LOG_IN_TERMNINAL:
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

# Write in file
today = datetime.now()
today = today.strftime('%Y_%m_%d')
filename = '%s.log' % today

# If file exist, remove it
if os.path.isfile(filename):
    os.remove(filename)

file_handler = logging.FileHandler(filename)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

# COM_PORT = 'COM3'
DB_URL = '139.150.72.146'
DB_USER = 'dbUser'
DB_PW = 'dbUser'
DB_NAME = 'bicycle_data'

class MainDialog(QDialog):
    def __init__(self):
        # Display minimize, close button
        super().__init__()
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        self.setWindowFlag(Qt.WindowCloseButtonHint, True)

        self.main_ui = Main_Ui()
        self.main_ui.setupUi(self)
        self.setWindowTitle('QT Sample Dialog')

        self.excel_file = None
        self.my_thread = None
        self.ser = None

        self.main_ui.btn_open_serial.clicked.connect(self.open_serial)
        self.main_ui.btn_close_serial.clicked.connect(self.close_serial)

        self.main_ui.btn_set_power.clicked.connect(self.set_power)
        self.main_ui.btn_get_power.clicked.connect(self.get_power)
        self.main_ui.btn_clear.clicked.connect(self.clear_log)

        self.main_ui.btn_find_excel.clicked.connect(self.find_excel)
        self.main_ui.btn_update_db.clicked.connect(self.update_db)
        self.main_ui.btn_export_to_excel.clicked.connect(self.export_db)
        self.main_ui.btn_exit.clicked.connect(self.close_dialog)

    def open_serial(self):
        try:

            serial_port = self.main_ui.cb_serial_port.currentText()
            # todo: 시리얼 객체 생성해서 self.ser에 할당하기
            # self.sef = ...

            QMessageBox.information(self, 'Information', f'{serial_port} is opened.', QMessageBox.Ok)

            # todo: 버튼 활성화/비활성화
            # 포트열기 : Disable
            # 포트닫기, 기능버튼 : Enable

        except Exception as e:
            self.ser = None
            QMessageBox.warning(self, 'Error', str(e), QMessageBox.Ok)

    def close_serial(self):
        try:
            self.ser.close()
            self.ser = None
            QMessageBox.information(self, 'Information', f'Serial post is closed.', QMessageBox.Ok)
            # todo: 버튼 활성화/비활성화
            # 포트열기 : Enable
            # 포트닫기, 기능버튼 : Disable

        except Exception as e:
            self.ser = None
            QMessageBox.warning(self, 'Error', str(e), QMessageBox.Ok)

    def export_db(self):
        # todo: from_date, region, file_name 값 설정하기
        # from_date = ...
        # region = ...
        # file_name = ...

        if '.xlsx' not in file_name:
            QMessageBox.warning(self, '경고', '잘못된 파일명입니다!!!', QMessageBox.Yes)
            return

        if from_date == '' or region == '':
            QMessageBox.warning(self, '경고', '설치날짜 또는 지역이 입력되지 않았습니다!!!', QMessageBox.Yes)
        else:
            self.get_data_from_db(from_date, region, file_name)
            self.main_ui.btn_export_to_excel.setEnabled(False)
            QMessageBox.information(self, '알림', '엑셀내보내기가 완료되었습니다.', QMessageBox.Yes)
            self.main_ui.btn_export_to_excel.setEnabled(True)

    def update_db(self):
        if self.excel_file is None:
            QMessageBox.warning(self, '경고', '선택된 파일이 없습니다!!!', QMessageBox.Yes)
        else:
            # 쓰레드
            interval = 0.1
            self.main_ui.btn_update_db.setEnabled(False)
            # todo: UploadThread 객체 생성 후 signal 셋팅 후 쓰레드 시작
            # self.my_thread = ... # 쓰레드 객체 생성
            # self.my_thread... # 시그널 설정
            # self.my_thread... # 쓰레드 시작

    def find_excel(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open file', './')

        if file_name:
            # todo: 엑셀파일명 LineEdit에 설정하기
            # self.main_ui.le_excel_path...
            self.excel_file = file_name
        else:
            QMessageBox.warning(self, '경고', '파일이 선택되지 않았습니다!!!', QMessageBox.Yes)

    def get_data_from_db(self, from_date, region, output_file_name):
        wb = Workbook()
        ws = wb.active

        ws.title = '공유자전거'

        ws['A1'] = '대여소번호'
        ws.merge_cells('A1:A5')

        ws['B1'] = '보관소(대여소)명'
        ws.merge_cells('B1:B5')

        ws['C1'] = '소재자(위치)'
        ws.merge_cells('C1:F2')

        ws['C3'] = '자치구'
        ws.merge_cells('C3:C5')

        ws['D3'] = '상세주소'
        ws.merge_cells('D3:D5')

        ws['E3'] = '위도'
        ws.merge_cells('E3:E5')

        ws['F3'] = '경도'
        ws.merge_cells('F3:F5')

        ws['G1'] = '설치시기'
        ws.merge_cells('G1:G5')

        ws['H1'] = '설치형태'
        ws.merge_cells('H1:I1')

        ws['H2'] = 'LCD'
        ws.merge_cells('H2:H3')

        ws['H4'] = '거치대수'
        ws.merge_cells('H4:H5')

        ws['I2'] = 'QR'
        ws.merge_cells('I2:I3')

        ws['I4'] = '거치대수'
        ws.merge_cells('I4:I5')

        ws['J1'] = '운영방식'
        ws.merge_cells('J1:J5')

        db = Database(DB_URL, DB_USER, DB_PW, DB_NAME)
        db.connect_db()

        sql = 'SELECT * FROM elias WHERE DATE(install_date) >= %s AND region = %s;'
        values = (from_date, region)
        data_list = db.execute_and_return(sql, values)

        # todo: 엑셀에 DB에서 가져온 데이터 작성하기
        for data in data_list:
            #...
            pass

        thin_border = Border(left=Side(style='thin'),
                             right=Side(style='thin'),
                             top=Side(style='thin'),
                             bottom=Side(style='thin'))

        bold_white_font = Font(bold=True,
                               size=12,
                               italic=None,
                               underline=None,
                               strike=None,
                               color='FFFFFF')

        background_fill = PatternFill(start_color='525E75',
                                      end_color='525E75',
                                      fill_type='solid')

        # todo: 헤더에 스타일 적용하기
        # ...

        # todo: 전체 테이블에 테두리 적용하기
        # ...

        wb.save(output_file_name)

    def clear_log(self):
        self.main_ui.tb_log_power.clear()

    def set_power(self):
        is_power_on = self.main_ui.rb_on.isChecked()

        # todo: 명령어 작성
        if is_power_on:
            # command = ...
            pass
        else:
            # command = ...
            pass

        self.add_log('=' * 30)
        self.add_log(f'Send Command: {command.decode()[:-1]}')

        # todo: 포트에 명령어 전송
        # ...

        # todo: 포트로 부터 응당값 가져오기
        # resp = ...
        self.add_log(f'Response: {resp.decode()[:-1]}')

    def get_power(self):
        # todo: 명령어 작성
        # command =

        self.add_log('=' * 30)
        self.add_log(f'Send Command: {command.decode()[:-1]}')

        # todo: 명령어를 포트에 전송
        # ...

        # todo: 포트로 부터 응당값 가져오기
        # resp = ...
        self.add_log(f'Response: {resp.decode()[:-1]}')

        # todo: resp를 parsing하여 power_state값 적용하기
        # power_state = ...

        if power_state == '01':
            self.main_ui.rb_on.setChecked(True)
            self.main_ui.rb_off.setChecked(False)
        else:
            self.main_ui.rb_on.setChecked(False)
            self.main_ui.rb_off.setChecked(True)

    @pyqtSlot()
    def thread_is_stopped(self):
        QMessageBox.information(self, '알림', 'DB 업로드가 완료되었습니다.', QMessageBox.Yes)
        self.main_ui.btn_update_db.setEnabled(True)

    def add_log(self, message):
        now = datetime.now()
        now = now.strftime("%H:%M:%S")
        log_message = '[%s]: %s' % (now, message)
        self.main_ui.tb_log_power.append(log_message)
        logger.info(message)

    def close_dialog(self):
        sys.exit(0)

    # ESC 무시
    def key_press_event(self, event):
        if not event.key() == Qt.Key_Escape:
            pass

class UploadThread(QThread):
    stopSignal = pyqtSignal()

    def __init__(self, excel_file_name, interval=10):
        super(self.__class__, self).__init__()
        self.excel_file_name = excel_file_name
        self.isRunning = True
        self.interval = interval

    def put_data_to_db(self):
        wb = load_workbook(self.excel_file_name)
        ws = wb.active

        db = Database(DB_URL, DB_USER, DB_PW, DB_NAME)
        db.connect_db()

        columns = ['station_number', 'station_name', 'region', 'address', 'latitude', 'longitude',
                   'install_date', 'lcd_count', 'qr_count', 'proc_type']
        # todo: 엑셀에서 데이터 읽어와서 DB에 insert 하기
        for row in ws.iter_rows(min_row=6):
            # ...
            pass

        db.commit_only()

    def run(self):
        self.put_data_to_db()
        self.stopSignal.emit()

    def stop(self):
        self.isRunning = False
        self.logSignal.emit('Thread is stopping')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MainDialog()
    myWindow.show()
    app.exec()