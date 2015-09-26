import sys
import os.path
from srtmod import srtmod

def main(): 
    if len(sys.argv) < 5:
        print 'Usage: ' + sys.argv[0] +' <filename> <time amount> <time part>' \
            +' <operation> '
        print 'time part: (S)econds or (M)inutes'
        print 'operation: (/A)dd or (/D)iscount'
    else:
        try:
            file_name = sys.argv[1]
            time_amount = int(sys.argv[2])
            time_part = sys.argv[3]
            if time_part not in ('S', 'M'):
                raise ValueError('Time part should be S or M')
            operation = sys.argv[4]
            if operation not in ('/A', '/D'):
                raise ValueError('Operation should be /A or /D')
            srt = srtmod.SrtMod(file_name, time_amount, time_part, operation)
            if srt.process():
                print 'Subtitle file was created successfully'
                print 'file saved at :' + os.path.splitext(file_name)[0] + '(modified).srt'
        except OverflowError:
            print 'Exception: Invalid time amount for this operation'
        except ValueError as ex:
            print 'Exception: ' + str(ex)

if __name__ == '__main__':
    main()