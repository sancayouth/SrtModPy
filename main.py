import os.path
import argparse
from srtmod.srtmod import SrtMod


def main():
    parser = argparse.ArgumentParser(prog='SrtModPy',\
            description='Just adjusts the timing of subtitle files')
    parser.add_argument('file', help='the subtitle to be modified')
    parser.add_argument('time_amount', type=float,\
           help='the amount of time to be added or subtracted to subtitle')
    parser.add_argument('-t',\
           help='it\'s the part of time to be modified', choices=['S', 'M'], default='S')
    parser.add_argument('-o',\
           help='add or discount time to subtitle', choices=['/A', '/D'], default='/A')
    arg = parser.parse_args()

    time_amount = arg.time_amount
    file_ = arg.file
    time_part = arg.t
    operation = arg.o
    try:
        srt = SrtMod(file_, time_amount, time_part, operation)
        if srt.process():
			print 'subtitle file was created successfully'
			print 'file saved at: ' + os.path.splitext(file_)[0] +'(modified).srt'
        else:
            print '\nsubtitle can not be processed'
    except OverflowError:
        print 'Exception: Invalid time amount for this operation'

if __name__ == '__main__':
    main()
