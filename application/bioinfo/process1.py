# coding=utf-8

import os
import pandas as pd


def process1_1(process):
    file_path = os.path.join(process['data_dir'], process['source_file'])
    df = pd.read_excel(file_path, dtype={'age_at_initial_pathologic_diagnosis': str,
                                         'days_to_birth': str,
                                         'days_to_last_followup': str,
                                         'days_to_death': str})

    columns = ['sampleID', 'age_at_initial_pathologic_diagnosis', 'days_to_birth', 'gender', 'pathologic_T',
               'pathologic_M', 'pathologic_N', 'pathologic_stage', 'days_to_last_followup', 'days_to_death']

    df_output1 = df[columns][(df['sampleID'].str[-2:].astype('int') < 11) &
                             (df['new_neoplasm_event_type'].isnull()) &
                             (df['pathologic_M'] == 'M0') &
                             (df['pathologic_N'] == 'N0')]

    df_output2 = df[columns][(df['sampleID'].str[-2:].astype('int') < 11) &
                             ((df['new_neoplasm_event_type'] == 'Distant Metastasis') |
                              (df['pathologic_M'] == 'M1') |
                              (df['pathologic_N'] == 'N1') |
                              (df['pathologic_N'] == 'N1b'))]

    file_path = os.path.join(process['data_dir'], process['output_file'])
    writer = pd.ExcelWriter(file_path, engine='xlsxwriter', options={'strings_to_numbers': True})
    df_output1.to_excel(writer, sheet_name='Metastasis group', index=False)
    df_output2.to_excel(writer, sheet_name='Non-metastasis group', index=False)
    writer.save()
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
