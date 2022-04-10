# -*- coding: utf-8 -*-
import os.path
import re
from datetime import timedelta, datetime
from dataclasses import dataclass, field
from typing import List

@dataclass
class SrtMod(object):
    content: List[str] = field(init=False)
    filename: str 
    time_amount: int = field(default= 0)
    time_part: str  = field(default='S')
    operation: str = field(default='')

    def __post_init__(self) -> None:
        self.time_part = self.time_part.upper()
        self.operation = self.operation.upper()
        if self.time_part == 'M':
            self.time_amount *= 60
        if self.operation == 'D' and self.time_amount > 0:
            self.time_amount *= -1

    def check_file_extension(self) -> bool:
        return '.srt' in os.path.splitext(self.filename)[1]

    def file_exist(self) -> bool:
        return os.path.exists(self.filename)

    def mod_time(self, g_time: str) -> str:
        a = datetime(1, 1, 1, int(g_time.group(1)), int(g_time.group(2)),\
             int(g_time.group(3)))
        b = a + timedelta(seconds=self.time_amount)
        micrseg = g_time.group(4)
        return '%s:%s:%s,%s' % ( str(b.hour).zfill(2), str(b.minute).zfill(2),
                str(b.second).zfill(2), micrseg, )

    def mod_line(self, line) -> str:
        mat = re.match(r'(\d[\S.]+) --> ([\S.]+)', line)
        if mat:
            expression = r'(\d+):(\d+):(\d+),(\d{3})'
            begin = re.match(expression, mat.group(1))
            end = re.match(expression, mat.group(2))
            line = f'{self.mod_time(begin)} --> {self.mod_time(end)}\n'
        return line

    def save_to_file(self) -> None:
        name = os.path.splitext(self.filename)[0] + '(modified).srt'
        with open(name, 'w') as f:
            f.writelines(self.content)

    def process(self) -> bool:
        result = False
        if self.check_file_extension() and self.file_exist():
            with open(self.filename, 'r') as f:
                self.content = [ self.mod_line(line) for line in f.readlines() ]
            self.save_to_file()
            result = True
        return result
