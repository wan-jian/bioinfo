# coding=utf-8

from application.utilities.xlsparser import Workbook, Sheet
from application import app


def process1_1():
    workbook = Workbook()
    workbook.read_xls(file_name=app.proj['source_file'])
    sheet = workbook.get_sheet_by_index(0)

    sheet1 = Sheet()
    sheet2 = Sheet()
    sheet1.set_name('Metastasis group')
    sheet2.set_name('Non-metastasis group')
    header = ['sampleID', 'age_at_initial_pathologic_diagnosis', 'days_to_birth', 'gender', 'pathologic_T',
              'pathologic_M', 'pathologic_N', 'pathologic_stage','days_to_last_followup', 'days_to_death']
    sheet1.set_header(header)
    sheet2.set_header(header)

    for r in range(len(sheet.rows)):
        row = []
        for col_name in header:
            item = sheet.get_item_by_name(r, col_name)
            row.append(item)

        v = row[sheet1.get_header_index('sampleID')]
        if int(v[-2:]) >= 11:
            continue

        v = sheet.get_item_by_name(r, 'new_neoplasm_event_type')
        v1 = row[sheet1.get_header_index('pathologic_M')]
        v2 = row[sheet1.get_header_index('pathologic_N')]
        if v1 == 'M0' and v2 == 'N0' and v == '':
            sheet1.append_row(row)

        if v1 == 'M1' or v2 == 'N1'or v2 == 'N1b' or v == 'Distant Metastasis':
            sheet2.append_row(row)

    workbook = Workbook()
    workbook.append_sheet(sheet1)
    workbook.append_sheet(sheet2)

    workbook.write_xls(app.proj['output_file'])
