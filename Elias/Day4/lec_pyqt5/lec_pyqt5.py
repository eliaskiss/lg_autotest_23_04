# pip install pyqt5
# pip install pyside2 --> python 3.11은 설치안됨: pyside6 설치

import inspect
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QThread, pyqtSlot, pyqtSignal

import logging
from datetime import datetime
import os
import sys
import time

from main_ui import Ui_Dialog as Main_Ui

DISPLAY_LOG_IN_TERMNINAL = True

logger = logging.getLogger('MyLogger')
logger.setLevel(logging.INFO)
# http://oniondev.egloos.com/v/9603983
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

        self.my_thread = None

        self.main_ui.btn_exit.clicked.connect(self.close_dialog)

        # Thread
        self.main_ui.btn_start.clicked.connect(self.start_thread)
        self.main_ui.btn_stop.clicked.connect(self.stop_thread)

        # Line Edit
        self.main_ui.btn_get_le.clicked.connect(self.get_le)
        self.main_ui.btn_set_le.clicked.connect(self.set_le)

        # Spin Box
        self.main_ui.spinBox.setSingleStep(1)
        self.main_ui.btn_get_sp.clicked.connect(self.get_sp)
        self.main_ui.btn_set_sp.clicked.connect(self.set_sp)

        # Radio Button
        self.main_ui.btn_get_rb.clicked.connect(self.get_rb)
        self.main_ui.btn_set_rb.clicked.connect(self.set_rb)

        # List Widget
        self.lw_count = 0
        self.main_ui.btn_add_list.clicked.connect(self.add_lw)
        self.main_ui.btn_remove_list.clicked.connect(self.delete_lw)
        self.main_ui.listWidget.clicked.connect(self.select_row_lw)
        self.main_ui.btn_get_list.clicked.connect(self.get_list_lw)

        # Table Widget
        self.tableWidgetInit()
        self.main_ui.btn_get_tablewidget_item.clicked.connect(self.get_item)

        # MessageBox
        self.main_ui.btn_information.clicked.connect(self.box_info)
        self.main_ui.btn_warning.clicked.connect(self.box_warning)
        self.main_ui.btn_question.clicked.connect(self.box_question)

        # Disable, Enable
        self.main_ui.btn_enable.clicked.connect(self.enable_exit_button)
        self.main_ui.btn_disable.clicked.connect(self.disable_exit_button)

    ####################################################################
    # Enable/Disable Button
    def enable_exit_button(self):
        self.main_ui.btn_exit.setEnabled(True)
        self.main_ui.gb_le.setEnabled(True)

    def disable_exit_button(self):
        self.main_ui.btn_exit.setEnabled(False)
        self.main_ui.gb_le.setEnabled(False)

    ######################################################################################
    # MessageBox
    def box_question(self):
        # result = QMessageBox.question(self, 'Question', 'Do you delete?', QMessageBox.Ok, QMessageBox.Cancel)
        result = QMessageBox.question(self, 'Question', 'Do you delete?', QMessageBox.Yes, QMessageBox.No)
        if result == QMessageBox.Yes:
            self.add_log('Yes')
        else:
            self.add_log('No')

    def box_warning(self):
        result = QMessageBox.warning(self, 'Warning', 'Wrong Information', QMessageBox.Yes)
        if result == QMessageBox.Yes:
            self.add_log('Yes')
        else:
            self.add_log('No')

    def box_info(self):
        result = QMessageBox.information(self, 'Information', 'Success', QMessageBox.Yes)
        if result == QMessageBox.Yes:
            self.add_log('Yes')
        else:
            self.add_log('No')

    ###########################################################################################
    # TableWidget
    def tableWidgetInit(self):
        columns = ['Name', 'Address', 'Age']
        self.main_ui.tableWidget.setColumnCount(len(columns))
        self.main_ui.tableWidget.setHorizontalHeaderLabels(columns)
        self.main_ui.tableWidget.setColumnWidth(0, 89)
        self.main_ui.tableWidget.setColumnWidth(1, 100)
        self.main_ui.tableWidget.setColumnWidth(2, 80)

        table_data = [['Kim', 'Seoul', '20'],
                      ['Park', 'Busan', '20'],
                      ['Lee', 'Daegu', '20']]
        self.main_ui.tableWidget.setRowCount(len(table_data))

        for i, data in enumerate(table_data):
            for j in range(len(data)):
                item = QTableWidgetItem(data[j])
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
                item.setFlags(Qt.ItemIsEnabled)
                self.main_ui.tableWidget.setItem(i, j, item)

    def get_item(self):
        row = int(self.main_ui.le_row.text())
        column = int(self.main_ui.le_column.text())
        self.add_log('TableWidget Item[%s,%s]: %s' % (row, column, self.main_ui.tableWidget.item(row, column).text()))

    ###########################################################################################
    # ListWidget
    def add_lw(self):
        self.lw_count += 1
        self.main_ui.listWidget.addItem(f'Hello: {self.lw_count}')

    def delete_lw(self):
        current_row = self.main_ui.listWidget.currentRow()
        self.main_ui.listWidget.takeItem(current_row)

    def select_row_lw(self):
        current_row = self.main_ui.listWidget.currentRow()
        self.add_log(f'CurrentRow: {current_row}')

    def get_list_lw(self):
        items = []
        for i in range(self.main_ui.listWidget.count()):
            items.append(self.main_ui.listWidget.item(i).text())
        self.add_log(f'ListWidget: {items}')

    ###########################################################################################
    # LineEdit
    def get_le(self):
        value = self.main_ui.lineEdit.text()
        self.add_log('LineEdit: %s' % value)

    def set_le(self):
        self.main_ui.lineEdit.setText('world')

    ###########################################################################################
    # SpinBox
    def get_sp(self):
        value = self.main_ui.spinBox.value()
        self.add_log('SpinBox: %s' % value)

    def set_sp(self):
        self.main_ui.spinBox.setValue(10)

    ###########################################################################################
    # RadioButton
    def get_rb(self):
        value = self.main_ui.radioButton_a.isChecked()
        self.add_log('RadioButton A: %s' % value)
        value = self.main_ui.radioButton_b.isChecked()
        self.add_log('RadioButton B: %s' % value)
        value = self.main_ui.checkBox.isChecked()
        self.add_log('CheckBox: %s' % value)

    def set_rb(self):
        self.main_ui.radioButton_a.setChecked(True)
        self.main_ui.radioButton_b.setChecked(False)
        self.main_ui.checkBox.setChecked(True)

    ###########################################################################################
    # For Thread
    def start_thread(self):
        try:
            self.main_ui.progressBar.setMinimum(0)
            self.main_ui.progressBar.setMaximum(100)
            self.main_ui.progressBar.setValue(0)

            interval = 0.1
            self.my_thread = SomethingThread(None, interval)
            self.my_thread.logSignal.connect(self.add_log)
            self.my_thread.stopSignal.connect(self.thread_is_stopped)
            self.my_thread.countSignal.connect(self.count)
            self.my_thread.start()

            self.set_enable_buttons(False)
        except Exception as e:
            print('--> Exception is "%s" (Line: %s)' % (e, sys.exc_info()[-1].tb_lineno))

    def stop_thread(self):
        if self.my_thread is not None:
            self.my_thread.stop()

    def set_enable_buttons(self, enable):
        self.main_ui.btn_start.setEnabled(enable)
        self.main_ui.btn_stop.setEnabled(not enable)
    ###########################################################################################
    # Signal pyqtslot
    @pyqtSlot(int)
    def count(self, count):
        self.add_log('ProgressBar Value: %s' % count)
        self.main_ui.progressBar.setValue(count)

    @pyqtSlot()
    def thread_is_stopped(self):
        self.set_enable_buttons(True)

    @pyqtSlot(str)
    def add_log(self, message):
        now = datetime.now()
        now = now.strftime("%H:%M:%S")

        # 호출된 함수와 라인번호 가져오기
        curframe = inspect.currentframe()
        callframe = inspect.getouterframes(curframe, 2)
        func_name = callframe[1].function
        line_no = callframe[1].lineno

        log_message = f'[{now}]: {message} | Function:{func_name} Line No:{line_no}'
        file_message = f'{message} | Function:{func_name} Line No:{line_no}'
        self.main_ui.tb_log.append(log_message)
        logger.info(file_message)
    ###########################################################################################

    def close_dialog(self):
        sys.exit(0)

    # ESC 무시
    def key_press_event(self, event):
        if not event.key() == Qt.Key_Escape:
            pass

class SomethingThread(QThread):
    logSignal = pyqtSignal(str)
    countSignal = pyqtSignal(int)
    stopSignal = pyqtSignal()

    def __init__(self, param, interval=10):
        super(self.__class__, self).__init__()
        self.param = param
        self.isRunning = True
        self.interval = interval

    def run(self):
        self.logSignal.emit('Thread is started')
        count = 1
        while self.isRunning:
            time.sleep(self.interval)
            self.countSignal.emit(count)
            count += 1

            if count > 100:
                break

        self.logSignal.emit('Thread is stopped')
        self.stopSignal.emit()

    def stop(self):
        self.isRunning = False
        self.logSignal.emit('Thread is stopping')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MainDialog()
    myWindow.show()
    app.exec()