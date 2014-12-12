#!/usr/bin/python
import sys
import glob
import datetime

import argparse

from xunit2html import render_report


def main(args):
    parser = argparse.ArgumentParser(description="X2H, a tool for converting xunit generated xml files into a beautiful html report.")
    parser.add_argument('files',
                        action='store',
                        type=str,
                        metavar="xunit-file.xml",
                        nargs='+',
                        help="an xunit format xml file.")
    parser.add_argument('--output-file', '-o',
                        action='store',
                        default='report_%s.html' % datetime.datetime.now().strftime("%Y%m%dT%H%M%S"),
                        type=str,
                        metavar="outputfile.html",
                        dest="report_file")
    parser.add_argument('--show-successful-tests', '-s',
                        action='store_true',
                        help="display the successful tests in the report",
                        dest='show_successes')
    parsed_args = parser.parse_args(args)
    xunit_filenames = reduce(lambda x, y: x + y, [glob.glob(entry) for entry in parsed_args.files])
    report_filename = parsed_args.report_file
    with open(report_filename, 'w') as rfile:
        rfile.write(render_report(xunit_filenames, show_successes=parsed_args.show_successes))


if __name__ == '__main__':
    main(sys.argv[1:])
