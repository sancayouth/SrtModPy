# -*- coding: utf-8 -*-
import re
import unittest
from srtmod.srtmod import SrtMod


class Tests(unittest.TestCase):

    def test_correct_file_extension(self):
        srt = SrtMod('lalala.srt')
        result = srt.check_file_extension()
        self.assertTrue(result)

    def test_incorrect_file_extension(self):
        srt = SrtMod('lalala.txt')
        result = srt.check_file_extension()
        self.assertFalse(result)

    def test_file_exists(self):
        srt = SrtMod('sub.srt')
        result = srt.file_exist()
        self.assertTrue(result)

    def test_increment_fiften_seconds_to_time(self):
        srt = SrtMod('sub.srt', 15)
        part = '00:00:03,000'
        begin = re.match(r'(\d+):(\d+):(\d+),(\d{3})', part)
        mod = srt.mod_time(begin)
        self.assertEqual('00:00:18,000', mod)

    def test_increment_sixty_seconds_to_time(self):
        srt = SrtMod('sub.srt', 60)
        part = '00:00:03,000'
        begin = re.match(r'(\d+):(\d+):(\d+),(\d{3})', part)
        mod = srt.mod_time(begin)
        self.assertEqual('00:01:03,000', mod)

    def test_decrement_fiften_seconds_to_time(self):
        srt = SrtMod('sub.srt', 15, 'S', 'D')
        part = '00:00:30,000'
        begin = re.match(r'(\d+):(\d+):(\d+),(\d{3})', part)
        mod = srt.mod_time(begin)
        self.assertEqual('00:00:15,000', mod)

    def test_decrement_sixty_seconds_to_time(self):
        srt = SrtMod('sub.srt', 60, 'S', 'D')
        part = '00:01:03,000'
        begin = re.match(r'(\d+):(\d+):(\d+),(\d{3})', part)
        mod = srt.mod_time(begin)
        self.assertEqual('00:00:03,000', mod)

    def test_increment_ten_seconds_to_time_line(self):
        srt = SrtMod('sub.srt', 10, 'S')
        line = '00:00:03,000 --> 00:00:04,992'
        mod = srt.mod_line(line)
        self.assertEqual('00:00:13,000 --> 00:00:14,992\n', mod)

    def test_decrement_ten_seconds_to_time_line(self):
        srt = SrtMod('sub.srt', 10, 's', 'd')
        line = '00:00:13,000 --> 00:00:14,992'
        mod = srt.mod_line(line)
        self.assertEqual('00:00:03,000 --> 00:00:04,992\n', mod)

    def test_increment_fiften_seconds_to_time_line(self):
        srt = SrtMod('sub.srt', 15, 's')
        line = '00:00:03,000 --> 00:00:04,992'
        mod = srt.mod_line(line)
        self.assertEqual('00:00:18,000 --> 00:00:19,992\n', mod)

    def test_increment_one_minute_to_time_line(self):
        srt = SrtMod('sub.srt', 1, 'm')
        line = '00:00:03,000 --> 00:00:04,992'
        mod = srt.mod_line(line)
        self.assertEqual('00:01:03,000 --> 00:01:04,992\n', mod)

    def test_decrement_one_minute_to_time_line(self):
        srt = SrtMod('sub.srt', 1, 'm', 'D')
        line = '00:15:03,000 --> 00:16:04,992'
        mod = srt.mod_line(line)
        self.assertEqual('00:14:03,000 --> 00:15:04,992\n', mod)

    def test_decrement_to_negative_time(self):
        srt = SrtMod('sub.srt', -60, 'S', 'D')
        part = '00:00:03,000'
        begin = re.match(r'(\d+):(\d+):(\d+),(\d{3})', part)
        self.assertRaises(OverflowError, srt.mod_time, begin)

    def test_file_cannot_be_processed(self):
        srt = SrtMod('lalala.srt', 1, 'm', 'd')
        result = srt.process()
        self.assertFalse(result)

    def test_file_can_be_processed(self):
        srt = SrtMod('sub.srt', 1, 's', 'a')
        result = srt.process()
        self.assertTrue(result)
