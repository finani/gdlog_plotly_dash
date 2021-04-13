#!/usr/bin/env python3

import sys
import gdlog_plot
import gdlog_parser

if __name__ == '__main__':
    if len(sys.argv) == 1: # for test run
        csv_path = "gdLog_210323_172626.csv"
        print("Test run gdlog_plot.py using \'gdLog_210323_172626.csv\'\n")
        print("\tUsage: python3 gdlog_plot.py path_of_your_csv_file\n")
    elif len(sys.argv) == 2:
        csv_path = sys.argv[1]
    else:
        raise SystemExit('\tUsage: python3 %s path_of_your_csv_file or path_of_your_bin_file' % sys.argv[0])

    file_extension = csv_path.split('/')[-1].split('.')[1]

    if file_extension == 'bin':
        gdlog_parser = gdlog_parser.GDLOG_PARSER(csv_path)
        gdlog_parser.run()
    elif file_extension == 'csv':
        gdlog_plotter = gdlog_plot.GDLOG_PLOTTER(csv_path)
        gdlog_plotter.show_guide()
        while(True):
            gdlog_plotter.run()
