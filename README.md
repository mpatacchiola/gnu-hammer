
Collection of simple tools for Unix systems which I realised for solving basic tasks.

midwife
--------

Midwife allows tracking all the new files and folders generated in a specific root directory (including all the sub-folders). It is useful to implement rudimentary sandboxes. To compile the programme it is necessary to have a recent version of g++ which implements the [filesystem library](http://en.cppreference.com/w/cpp/experimental/fs). Using g++ 7.0 it is possible to compile as follows:

```
g++-7 -std=c++1z -O3 midwife.cpp -lstdc++fs -o ./midwife
```

The executable takes the following parameters as input:

1. -d, --destination: the absolute path of the folder to track (default ./)
2. -s, sleep: define the time (in milliseconds) between calls (default 1000)

The output produced by midwife is a string which identifies the absolute path of a new file/folder which has been generated.
The output can be easily redirected in a log file:

```
midwife --destination /home/user/program --sleep 1000 >> log.txt
```

gregory
--------

Gregory is a python script based on the `datetime` module which can generate a list of dates based on user-defined criteria. The output can be redirected in a text file.
To **install** the module follow this procedure:

```
sudo cp gregory.py /usr/local/bin/gregory
sudo chmod +x /usr/local/bin/gregory
```

The **optional parameters** for gregory are summarised here:

```
optional arguments:
  -h, --help            show this help message and exit
  -o PATH_OUTPUT, --output PATH_OUTPUT
                        path to an output file
  -s START_DATE, --start START_DATE
                        start-date in format: DD/MM/YYYY
  -e END_DATE, --end END_DATE
                        end-date in format: DD/MM/YYYY
  -d DIVIDER_CHAR, --divide DIVIDER_CHAR
                        divide the date members using this character (default:
                        none)
  -t, --twin            if given allows the presence of duplicated dates in
                        case of single and double-format
  -q, --quiet           if given does not print any info on terminal. Useful
                        for pipelines.
  -c, --capital         if given sets the first letter of days (A) and months
                        (B) as capital
  -C, --CAPITAL         if given sets all the letters of days (A) and months
                        (B) as capital
  -l LOCALE, --locale LOCALE
                        set the locale language, it is used to generate months
                        and days names
  -f [FORMAT_LIST [FORMAT_LIST ...]], --format [FORMAT_LIST [FORMAT_LIST ...]]
                        list of formats to produce (default: all-formats). It
                        can be any combination of year-mont-day. Capital
                        letters identify the zero-padded spelling for days (D)
                        and months (M), and the four-letters notation for
                        years (Y). Lower-case letters identify non-zero-padded
                        notation for days (d) and months (m), and the two-
                        letters notation for years (y). Month can be
                        represented as full locale name (B) or abbreviated
                        name (b). The date 01/02/2003 can be represented as
                        follows: dmy=1203, DMY=01022003, dMY=1022003,
                        Ymd=200321, YMD=20030201, DBY=01February2003,
                        DbY=01Feb2003
```

Now some **examples** of usage. To print on terminal all the dates between a starting point (-s) 01/01/2001 and today in format day/month/year:

```
gregory -q -s 01/01/2001 -f DMY
```

```
01012001
02012001
03012001
...
```

To print on terminal all the dates between a starting point (-s) 01/01/2001 and an ending point (-e) 05/01/2001 in format day/month:

```
gregory -q -s 01/01/2001 -e 05/01/2001 -f DM
```

```
0101
0201
0301
0401
```

To print the same range showing full-name for days and months:

```
gregory -q -s 01/01/2001 -f ABY
```

```
mondayjanuary2001
tuesdayjanuary2001
wednesdayjanuary2001
thursdayjanuary2001
...
```

Printing the same range with a separator (-d) and starting capital letter (-c) for days and months:

```
gregory -q -s 01/01/2001 -f ABY -d '/' -c
```

```
Monday/January/2001
Tuesday/January/2001
Wednesday/January/2001
...
```

To save on a file called `date.txt` and show statistics:

```
gregory -s 01/01/2001 -f ABY -o 'date.txt' 
```

```
Start date .................. 01/01/2001
End date .................... 03/09/2017
Total days .................. 6089
Total lines worst case ...... 6089
Size worst case (bytes) ..... ~108993
Size worst case (MB)    ..... ~0.11
You have 5 seconds to abort...
Started!
Done!
```

