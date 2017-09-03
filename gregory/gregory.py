#!/usr/bin/python


# gregory generates date ranges based on the Gregorian calendar
# Copyright (C) 2017  Massimiliano Patacchiola
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#Installation:
#sudo cp gregory.py /usr/local/bin/gregory
#sudo chmod +x /usr/local/bin/gregory

#Examples of usage:
#gregory -q -s 01/01/2001 -e 05/01/2001 -f DMY
#gregory -q -s 01/01/2001 -f DMY

import datetime
import time
import argparse
import locale

DEBUG = False

# Check if a date is in a valid format
def check_date(s):
    try:
        return datetime.datetime.strptime(s, "%d/%m/%Y")
    except ValueError:
        msg = "the date '" + s + "' is not valid!" 
        raise argparse.ArgumentTypeError(msg)


def main():
    # Parse the input args 
    parser = argparse.ArgumentParser(prog='gregory', description='Generate Gregorian-date lists based on user criteria.')
    parser.add_argument('-o', '--output', dest='path_output', default='', required=False, help='path to an output file')
    parser.add_argument('-s', '--start', dest='start_date', required=True, type=check_date, help='start-date in format: DD/MM/YYYY')
    parser.add_argument('-e', '--end', dest='end_date', required=False, default=datetime.datetime.now(), type=check_date, help='end-date in format: DD/MM/YYYY')
    parser.add_argument('-d', '--divide', dest='divider_char', default='', required=False, type=str, help='divide the date members using this character (default: none)')
    parser.add_argument('-t', '--twin', action='store_true', default=False, required=False, help='if given allows the presence of duplicated dates in case of single and double-format')
    parser.add_argument('-q', '--quiet', action='store_true', default=False, required=False, help='if given does not print any info on terminal. Useful for pipelines.')
    parser.add_argument('-c', '--capital', action='store_true', default=False, required=False, help='if given sets the first letter of days (A) and months (B) as capital')
    parser.add_argument('-C', '--CAPITAL', action='store_true', default=False, required=False, help='if given sets all the letters of days (A) and months (B) as capital')
    parser.add_argument('-l', '--locale', default='', required=False, type=str, help='set the locale language, it is used to generate months and days names (e.g. en_US.UTF-8, en_GB.UTF-8')
    parser.add_argument('-f', '--format', dest='format_list', nargs='*', default=[], help="list of formats to produce (default: all-formats). It can be any combination of year-mont-day. Capital letters identify the zero-padded spelling for days (D) and months (M), and the four-letters notation for years (Y). Lower-case letters identify non-zero-padded notation for days (d) and months (m), and the two-letters notation for years (y). Month can be represented as full locale name (B) or abbreviated name (b). The date 01/02/2003 can be represented as follows: dmy=1203, DMY=01022003, dMY=1022003, Ymd=200321, YMD=20030201, DBY=01February2003, DbY=01Feb2003")
    args = parser.parse_args()

    # List of all the accepted format
    format_accepted_list = ['d', 'a', 'm', 'b', 'y',
                            'D', 'A', 'M', 'B', 'Y',
                            'dm', 'DM', 'Dm', 'dM',
                            'db', 'DB', 'Db', 'dB',
                            'am', 'AM', 'Am', 'aM',
                            'ab', 'AB', 'Ab', 'aB',
                            'md', 'MD', 'mD', 'Md',
                            'bd', 'BD', 'bD', 'Bd',
                            'ma', 'MA', 'mA', 'Ma',
                            'ba', 'BA', 'bA', 'Ba',
                            'my', 'MY', 'mY', 'My',
                            'by', 'BY', 'bY', 'By',
                            'dy', 'DY', 'dY', 'Dy',
                            'ay', 'AY', 'aY', 'Ay',
                            'ym', 'YM', 'Ym', 'yM',
                            'yb', 'YB', 'Yb', 'yB',
                            'yd', 'YD', 'yD', 'Yd',
                            'ya', 'YA', 'yA', 'Ya',
                            'dmy', 'Dmy', 'dMy', 'dmY', 'DMy', 'DmY', 'dMY', 'DMY',
                            'amy', 'Amy', 'aMy', 'amY', 'AMy', 'AmY', 'aMY', 'AMY',
                            'dby', 'Dby', 'dBy', 'dbY', 'DBy', 'DbY', 'dBY', 'DBY',
                            'aby', 'Aby', 'aBy', 'abY', 'ABy', 'AbY', 'aBY', 'ABY',
                            'mdy', 'Mdy', 'mDy', 'mdY', 'MDy', 'MdY', 'mDY', 'MDY',
                            'may', 'May', 'mAy', 'maY', 'MAy', 'MaY', 'mAY', 'MAY',
                            'bdy', 'Bdy', 'bDy', 'bdY', 'BDy', 'BdY', 'bDY', 'BDY',
                            'bay', 'Bay', 'bAy', 'baY', 'BAy', 'BaY', 'bAY', 'BAY',
                            'ymd', 'Ymd', 'yMd', 'ymD', 'YMd', 'YmD', 'yMD', 'YMD',
                            'yma', 'Yma', 'yMa', 'ymA', 'YMa', 'YmA', 'yMA', 'YMA',
                            'ybd', 'Ybd', 'yBd', 'ybD', 'YBd', 'YbD', 'yBD', 'YBD',
                            'yba', 'Yba', 'yBa', 'ybA', 'YBa', 'YbA', 'yBA', 'YBA',
                            'ydm', 'Ydm', 'yDm', 'ydM', 'YDm', 'YdM', 'yDM', 'YDM',
                            'yam', 'Yam', 'yAm', 'yaM', 'YAm', 'YaM', 'yAM', 'YAM',
                            'ydb', 'Ydb', 'yDb', 'ydB', 'YDb', 'YdB', 'yDB', 'YDB',
                            'yab', 'Yab', 'yAb', 'yaB', 'YAb', 'YaB', 'yAB', 'YAB',
                            'dym', 'Dym', 'dYm', 'dyM', 'DYm', 'DyM', 'dYM', 'DYM',
                            'aym', 'Aym', 'aYm', 'ayM', 'AYm', 'AyM', 'aYM', 'AYM',
                            'dyb', 'Dyb', 'dYb', 'dyB', 'DYb', 'DyB', 'dYB', 'DYB',
                            'ayb', 'Ayb', 'aYb', 'ayB', 'AYb', 'AyB', 'aYB', 'AYB',
                            'myd', 'Myd', 'mYd', 'myD', 'MYd', 'MyD', 'mYD', 'MYD',
                            'mya', 'Mya', 'mYa', 'myA', 'MYa', 'MyA', 'mYA', 'MYA',
                            'byd', 'Byd', 'bYd', 'byD', 'BYd', 'ByD', 'bYD', 'BYD',
                            'bya', 'Bya', 'bYa', 'byA', 'BYa', 'ByA', 'bYA', 'BYA']

    # Check if the argument passed are valid string
    format_list = list()
    byte_counter = 0
    for format in args.format_list:
        if format not in format_accepted_list:
            if len(format) > 3:
                print "[ERROR] The format you passed is invalid '" + str(format) + "' it has more than 3 characters!"
            else:
                print "[ERROR] The format you passed '" + str(format) + "' is not valid!"
                print "Valid characters: d, m, y, D, M, Y, a, A, b, B"
            return
        else:
            format_list.append(format)
            # Evaluating how many bytes are stored
            for char in format:
                if char == 'd': byte_counter += 1.5 #only 9/30 days have 1 byte
                elif char == 'D': byte_counter += 2
                elif char == 'm': byte_counter += 1.3 # only 9/12 monts have 1 byte
                elif char == 'M': byte_counter += 2
                elif char == 'b': byte_counter += 3
                elif char == 'B': byte_counter += 6.1 # approximated as average
                elif char == 'a': byte_counter += 3
                elif char == 'A': byte_counter += 6.8 # approximated as average
                elif char == 'y': byte_counter += 2
                elif char == 'Y': byte_counter += 4
                if char != format[-1]:
                    byte_counter += len(args.divider_char)
    # Check lenght of format list
    if len(format_list) == 0:
        format_list = format_accepted_list
        byte_counter = 1093+ (120*len(args.divider_char))

    # Used for estimating the byte dimension of all-formats
    if DEBUG:
        counter = 0
        for format in format_accepted_list:
            for char in format:
                if char == 'd': counter += 1.5 #only 9/30 days have 1 byte
                elif char == 'D': counter += 2
                elif char == 'm': counter += 1.3 # only 9/12 monts have 1 byte
                elif char == 'M': counter += 2
                elif char == 'b': byte_counter += 3
                elif char == 'B': byte_counter += 6.1 # approximated as average
                elif char == 'a': byte_counter += 3
                elif char == 'A': byte_counter += 6.8 # approximated as average
                elif char == 'y': counter += 2
                elif char == 'Y': counter += 4
        print("[DEBUG] byte counter full format list: " + str(counter))

    # Estimating the output size and waiting...
    tot_days = (args.end_date-args.start_date).days
    #tot_months = (args.end_date-args.start_date).months
    #tot_years = (args.end_date-args.start_date).years
    tot_lines = tot_days * len(format_list)
    tot_bytes = (tot_days * byte_counter) + tot_lines
    if args.quiet == False:
        print("Start date .................. " + args.start_date.strftime("%d/%m/%Y"))
        print("End date .................... " + args.end_date.strftime("%d/%m/%Y"))
        print("Total days .................. " + str(tot_days))
        #print("Total months .............." + str(tot_months))
        #print("Total years   ..... " + str(tot_years))
        print("Total lines worst case ...... " + str(tot_lines))
        print("Size worst case (bytes) ..... ~" + str(int(tot_bytes)))
        print("Size worst case (MB)    ..... ~{0:.2f}".format(tot_bytes/1000000.0))
        print "You have 5 seconds to abort..."
        time.sleep(5)
        print("Started!")

    # Variable used when the twin argument is given
    is_clone = False
    if args.twin == False:
        unique_list = list()

    # Set the locale according to arg passed
    if args.locale != '':
        try:
            locale.setlocale(locale.LC_ALL, args.locale) # "en_GB.utf8")
        except:
            print "[WARNING] the locale '" + args.locale + "' is not supported by your system."
            return

    # Iterating
    for i in range(0, (args.end_date-args.start_date).days):
        date = args.start_date + datetime.timedelta(days=i)
        for format in format_list:
            date_string = ""
            for char in format:
                if char == 'd' and date.day < 10: date_string += date.strftime("%d").lstrip("0").replace("0", "")
                elif char == 'd' and date.day >= 10: date_string += date.strftime("%d")
                elif char == 'a': date_string += date.strftime("%a")
                elif char == 'A': date_string += date.strftime("%A")
                elif char == 'D': date_string += date.strftime("%d")
                elif char == 'm' and date.month < 10: date_string += date.strftime("%m").lstrip("0").replace("0", "")
                elif char == 'm' and date.month >= 10: date_string += date.strftime("%m")
                elif char == 'b': date_string += date.strftime("%b")
                elif char == 'B': date_string += date.strftime("%B")
                elif char == 'M': date_string += date.strftime("%m")
                elif char == 'y': date_string += date.strftime("%y")
                elif char == 'Y': date_string += date.strftime("%Y")
                if char != format[-1]:
                    date_string += args.divider_char
            # Check and apply capital letter command args
            if args.capital == False:
                date_string = date_string.lower()
            if args.CAPITAL == True:
                date_string = date_string.upper()
            # Check for twin if arg is given
            if args.twin == False:
                if not date_string in unique_list:
                    unique_list.append(date_string)
                    is_clone = False
                else:
                    is_clone = True
            # Print or write on file
            if is_clone==False:
                if args.path_output != '':
                    with open(args.path_output, "a") as myfile:
                        myfile.write(date_string + '\n')
                else:
                    print date_string

    # Finished and bye bye
    if args.quiet == False:
        print("Done!")

if __name__ == "__main__":
    main()
