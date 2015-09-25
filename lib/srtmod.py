# -*- coding: utf-8 -*-
import os.path
import re
from datetime import timedelta, datetime


class SrtMod:

    content = []
    content_aux = []

    def __init__(self, filename, cant=0, time_part='S', operation='/A'):
        self._file = filename
        self._cant = cant
        self._time_part = time_part.upper()
        self._operation = operation.upper()
        if self._time_part == 'M':
            self._cant *= 60
        if self._operation == '/D' and self._cant > 0:
            self._cant *= -1

    def check_file_extension(self):
        ext = os.path.splitext(self._file)[1]
        return ext == '.srt'

    def file_exist(self):
        return os.path.exists(self._file)

    def mod_time(self, g_time):
        a = datetime(1, 1, 1, int(g_time.group(1)), int(g_time.group(2)),
             int(g_time.group(3)))
        b = a + timedelta(seconds=self._cant)
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
        outputf = open('foo.srt', 'w')
        outputf.writelines(self.content_aux)
        outputf.close()

    def process(self):
        result = False
        if self.check_file_extension() and self.file_exist():
            with open('sub.srt', 'r') as f:
                self.content = f.readlines()
            for line in self.content:
                self.content_aux.append(self.mod_line(line))
            self.save_to_file()
            result = True
        return result
