# coding=utf-8

import xlrd
import xlwt


class Workbook:
    def __init__(self):
        self.sheets = []

    def read_xls(self, file_name):
        self.file_name = file_name
        wb = xlrd.open_workbook(file_name)
        for s in wb.sheets() :
            sheet = Sheet()
            sheet.name = s.name
            sheet.header = s.row_values(0)

            for i in range(1, s.nrows):
                sheet.rows.append(s.row_values(i))
            self.sheets.append(sheet)

    def write_xls(self, file_name):
        wb = xlwt.Workbook()
        for s in self.sheets:
            sheet = wb.add_sheet(s.name)
            for c in range(len(s.header)):
                sheet.write(0, c, s.header[c])
            for r in range(len(s.rows)):
                for c in range(len(s.header)):
                    sheet.write(r + 1, c, s.rows[r][c])

        wb.save(file_name)

    def get_sheet_by_index(self, index):
        return self.sheets[index]

    def get_sheet_by_name(self, name):
        for s in self.sheets:
            if s.name == name:
                return s
        return None

    def append_sheet(self, sheet):
        self.sheets.append(sheet)

class Sheet:
    def __init__(self):
        self.header = []
        self.rows = []
        self.name = ''

    def get_row(self, index):
        return self.rows(index)

    def get_item_by_name(self, row_index, col_name):
        row = self.rows[row_index]
        col = self.get_header_index(col_name)
        return row[col]

    def get_item_by_index(self, row_index, col_index):
        return self.rows[row_index][col_index]

    def get_header_index(self, col_name):
        for i in range(len(self.header)):
            if self.header[i] == col_name:
                return i
        return -1

    def set_header(self, header):
        self.header = header

    def append_row(self, row):
        self.rows.append(row)

    def set_name(self, name):
        self.name = name