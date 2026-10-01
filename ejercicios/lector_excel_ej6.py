from openpyxl import Workbook, load_workbook

wb = load_workbook(filename='inputs/sys_ejemplo.xlsx', data_only=True)
ws = wb.active

init_row=1

diccionario_vacio = {}

for row in ws.iter_rows():
    for cell in row:
        if (cell.value.lower() == 'código'):
            init_row = row
            break

for row in ws.iter_rows(min_row=init_row+1):
    for cell in row:
        if(cell.value != None):

        