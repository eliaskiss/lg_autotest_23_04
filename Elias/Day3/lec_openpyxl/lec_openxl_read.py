from openpyxl import load_workbook
from datetime import datetime, timedelta
from icecream import ic
import time

ic.configureOutput(includeContext=True)

file_name = 'trasfer_fee.xlsx'

# Open Excel File
wb = load_workbook(file_name,
                   read_only=True, # Read Only가 True이면, Lazy Loading이 발생해서 반드시 Close 해줘야만 핸드을 놓게됨
                   data_only=True) # Data Only가 True이면, cell의 함수 결과값을 가져옴

# Get Sheet list
ws_list = wb.sheetnames
ic(ws_list)

# Select Worksheet
# ws = wb.active # 현재 활성화되어 있는 sheet(저장할때 선택된 시트)
ws = wb['항공요금']
# ws = wb[ws_list[0]]  # 첫번째 워크시트
# ws = wb[ws_list[-1]] # 마지막번째 워크시트

