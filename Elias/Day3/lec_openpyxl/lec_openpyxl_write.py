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



wb.save(filename=file_name)
