import os.path
from srtmod.srtmod import SrtMod
import argparse


def main():
    parser = argparse.ArgumentParser(prog='SrtModPy',
            description='Just adjusts the timing of subtitle files')
    parser.add_argument('file_name', help='the subtitle to be modified')
    parser.add_argument('time_amount', metavar='time_amount', type=int,
           help='the amount of time to be added or subtracted to subtitle')
    parser.add_argument('time_part',
           help='it\'s the part of time to be modified', choices=['S', 'M'])
    parser.add_argument('operation',
           help='add or discount time to subtitle', choices=['/A', '/D'])
    r = parser.parse_args()
    time_amount = r.time_amount
    file_name = r.file_name
    time_part = r.time_part
    operation = r.operation
    try:
        srt = SrtMod(file_name, time_amount, time_part, operation)
        if srt.process():
            print '\nsubtitle file was created successfully'
            print 'file saved at :' + os.path.splitext(file_name)[0] \
                  + '(modified).srt'
        else:
            print '\nsubtitle can not be processed'
    except OverflowError:
        print 'Exception: Invalid time amount for this operation'


if __name__ == '__main__':
    main()