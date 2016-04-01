# -*- coding: utf-8 -*-
import os.path
import re
from datetime import timedelta, datetime


class SrtMod(object):

    content = []
    content_aux = []

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
        ext = os.path.splitext(self._file)[1]
        return ext == '.srt'

    def file_exist(self):
        return os.path.exists(self._file)

    def mod_time(self, g_time):
        a = datetime(1, 1, 1, int(g_time.group(1)), int(g_time.group(2)),\
             int(g_time.group(3)))
        b = a + timedelta(seconds=self.time_amount)
        micrseg = g_time.group(4)
        return  str(b.hour).zfill(2) + ':' + str(b.minute).zfill(2) + \
                      ':' + str(b.second).zfill(2) + ',' + micrseg

    def mod_line(self, line):
        mat = re.match(r'(\d[\S.]+) --> ([\S.]+)', line)
        if mat:
            expression = r'(\d+):(\d+):(\d+),(\d{3})'
            begin = re.match(expression, mat.group(1))
            res1 = self.mod_time(begin)
            end = re.match(expression, mat.group(2))
            res2 = self.mod_time(end)
            line = res1 + ' --> ' + res2 + '\n'
        return line

    def save_to_file(self):
        name = os.path.splitext(self._file)[0] + '(modified).srt'
        outputf = open(name, 'w')
        outputf.writelines(self.content_aux)
        outputf.close()

    def process(self):
        result = False
        if self.check_file_extension() and self.file_exist():
            with open(self._file, 'r') as f:
                self.content = f.readlines()
            for line in self.content:
                self.content_aux.append(self.mod_line(line))
            self.save_to_file()
            result = True
        return result
