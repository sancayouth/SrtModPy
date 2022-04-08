# -*- coding: utf-8 -*-
import os.path
import re
from datetime import timedelta, datetime


class SrtMod(object):

    content = []

    def __init__(self, filename, time_amount=0, time_part='S', operation='A'):
        self._file = filename
        self.time_amount = time_amount
        self.time_part = time_part.upper()
        self.operation = operation.upper()
        if self.time_part == 'M':
            self.time_amount *= 60
        if self.operation == 'D' and self.time_amount > 0:
            self.time_amount *= -1

    def check_file_extension(self):
        return '.srt' in os.path.splitext(self._file)[1]

    def file_exist(self):
        return os.path.exists(self._file)

    def mod_time(self, g_time):
        a = datetime(1, 1, 1, int(g_time.group(1)), int(g_time.group(2)),\
             int(g_time.group(3)))
        b = a + timedelta(seconds=self.time_amount)
        micrseg = g_time.group(4)
        return '%s:%s:%s,%s' % ( str(b.hour).zfill(2), str(b.minute).zfill(2),
                str(b.second).zfill(2), micrseg, )

    def mod_line(self, line):
        mat = re.match(r'(\d[\S.]+) --> ([\S.]+)', line)
        if mat:
            expression = r'(\d+):(\d+):(\d+),(\d{3})'
            begin = re.match(expression, mat.group(1))
            end = re.match(expression, mat.group(2))
            line = f'{self.mod_time(begin)} --> {self.mod_time(end)}\n'
        return line

    def save_to_file(self):
        name = os.path.splitext(self._file)[0] + '(modified).srt'
        with open(name, 'w') as f:
            f.writelines(self.content)

    def process(self):
        result = False
        if self.check_file_extension() and self.file_exist():
            with open(self._file, 'r') as f:
                self.content = [ self.mod_line(line) for line in f.readlines() ]
            self.save_to_file()
            result = True
        return result
