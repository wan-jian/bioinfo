# coding=utf-8

from application.utilities.xlsparser import Workbook, Sheet
import os
import pandas as pd

def process1_1(process):
    workbook = Workbook()
    file_path = os.path.join(process['data_dir'], process['source_file'])
    workbook.read_xls(file_name=file_path)
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

    file_path = os.path.join(process['data_dir'], process['output_file'])
    workbook.write_xls(file_path)
    print("Successfully write the result file: '{}'".format(process['output_file']))


def process1_2(process):
    file_path = os.path.join(process['data_dir'], process['source_file'][0])
    df1_1 = pd.read_excel(file_path, sheet_name='Metastasis group')
    df1_2 = pd.read_excel(file_path, sheet_name='Non-metastasis group')

    file_path = os.path.join(process['data_dir'], process['source_file'][1])
    df2 = pd.read_csv(file_path, sep='\t')

    df_result1 = rna_filter(df1_1, df2)
    df_result2 = rna_filter(df1_2, df2)

    file_path = os.path.join(process['data_dir'], process['output_file'][0])
    df_result1.to_csv(file_path, index=False, sep='\t')
    print("Successfully write the result file: '{}'".format(process['output_file'][0]))
    file_path = os.path.join(process['data_dir'], process['output_file'][1])
    df_result2.to_csv(file_path, index=False, sep='\t')
    print("Successfully write the result file: '{}'".format(process['output_file'][1]))

    file_path = os.path.join(process['data_dir'], process['source_file'][2])
    df2 = pd.read_csv(file_path, sep='\t')

    df_result1 = rna_filter(df1_1, df2)
    df_result2 = rna_filter(df1_2, df2)

    file_path = os.path.join(process['data_dir'], process['output_file'][2])
    df_result1.to_csv(file_path, index=False, sep='\t')
    print("Successfully write the result file: '{}'".format(process['output_file'][2]))
    file_path = os.path.join(process['data_dir'], process['output_file'][3])
    df_result2.to_csv(file_path, index=False, sep='\t')
    print("Successfully write the result file: '{}'".format(process['output_file'][3]))


def rna_filter(df1, df2):
    sample_ids = df1['sampleID']

    selected_columns = ['id']
    for column in df2.columns:
        for sampleID in sample_ids:
            if column[:15] == sampleID:
                selected_columns.append(column)

    df_result = df2[selected_columns]
    return df_result