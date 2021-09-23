# Tail

A Python implementation of the UNIX CLI Tail program that supports following.

## Usage

This program is intended to be used exactly as one would use the UNIX Tail 
program. From the Command Line Interface, invoke the program and specify the 
file to be be tailed. The last 10 lines of the file will be printed.

```
python tail.py path/to/file.txt
```

To print a different number of lines, use the `-n` option followed by the 
number of lines you wish to print:

```
python tail.py file.txt -n 5
```

Multiple files may be specified, in which case their tails will be preceded by 
a header indicating the file being printed:

```
python tail.py file_1.txt file_2.txt file_3.txt
```

Files may be followed with the `-f` option such that the program will remain 
active and print any new data appended to the file being followed (if 
specified, multiple files may also be followed simultaneously, with a single 
thread being responsible for each file being followed):

> Note: To end the program after the follow option is specified, use the Ctrl+C
command to send an interrupt signal.

```
python tail.py file.txt -f
```

To see a list of all options, specify the '-h' option

```
python tail.py -h
```
