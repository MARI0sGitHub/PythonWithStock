from openpyxl import load_workbook

def set(fileName):
    wb = load_workbook(fileName)
    ws = wb.active
    ws.column_dimensions['A'].width = 5
    ws.column_dimensions['B'].width = 10
    ws.column_dimensions['C'].width = 20
    ws.column_dimensions['D'].width = 100
    ws.column_dimensions['E'].width = 20
    ws.column_dimensions['F'].width = 15
    ws.column_dimensions['G'].width = 10
    ws.column_dimensions['H'].width = 5
    ws.column_dimensions['I'].width = 60
    wb.save(fileName)