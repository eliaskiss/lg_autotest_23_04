from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.drawing.image import Image
from datetime import datetime, timedelta
from openpyxl.chart import BarChart, Reference

# Create New Excel object
wb = Workbook()

file_name = './new_excel.xlsx'

# Get Active Worksheet
ws = wb.active # 'sheet1'

# Set Sheet Name
ws.title = 'Basic'

# Set Cell Value
ws['A1'] = 'Hello World'
ws['B1'] = 10
ws['C1'] = 20

# Insert Comment
comment = Comment('This is comment', 'Elias Kim', 100, 100)
ws['A1'].comment = comment

# Insert Row
row = [1,2,3,4,5]
ws.append(row)
# for i in range(10):
#     ws.append(row)

# Use Function
ws['D1'] = '=SUM(B1+C1)'

# Insert Datetime
ws['A4'] = datetime.now()
ws['B4'] = datetime.now() + timedelta(days=1) # 내일
# ws['B4'] = datetime.now() - timedelta(days=1) # 어제
# ws['B4'] = datetime.now() + timedelta(hours=1) # 한시간 후
ws['C4'] = '2023-04-12'

# Merge Target Cell
ws['F1'] = 'Hello'
ws['G1'] = 'World'

# # Merge/Unmerge
# ws.merge_cells(range_string='F1:G1')
# ws.unmerge_cells('F1:G1')

# Merge/Unmerge II
ws.merge_cells(start_row=1, start_column=6, end_row=1, end_column=7)
ws.unmerge_cells(start_row=1, start_column=6, end_row=1, end_column=7)
















wb.save(filename=file_name)
