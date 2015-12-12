import os.path
from srtmod.srtmod import SrtMod
import argparse


def main():
    parser = argparse.ArgumentParser(prog='SrtModPy',
            description='Just adjusts the timing of subtitle files')
    parser.add_argument('file', help='the subtitle to be modified')
    parser.add_argument('time_amount', type=float,
           help='the amount of time to be added or subtracted to subtitle')
    parser.add_argument('-t',
           help='it\'s the part of time to be modified', choices=['S', 'M'], default='S')
    parser.add_argument('-o',
           help='add or discount time to subtitle', choices=['/A', '/D'], default='/A')
    r = parser.parse_args()

    time_amount = r.time_amount
    file = r.file
    time_part = r.t
    operation = r.o
    
    try:
        srt = SrtMod(file, time_amount, time_part, operation)
        if srt.process():
            print 'subtitle file was created successfully'
            print 'file saved at: ' + os.path.splitext(file)[0] \
                  + '(modified).srt'
        else:
            print '\nsubtitle can not be processed'
    except OverflowError:
        print 'Exception: Invalid time amount for this operation'

if __name__ == '__main__':
    main()