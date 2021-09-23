# Tail

A Python implementation of the UNIX CLI Tail program that supports following.

## Installation

Download repository and open a Command Line Interface in the directory 
containing 'tail.py' and enter the command `pwd` to obtain the full path.
For the purpose of this example, let the full path be '/home/dev/Tail'.

Add the full path to the $PATH environment variable. To do so, first enter the 
following:

```
sudo nano ~/.bashrc
```

Now scroll to the bottom of the bashrc file in the now opened editor, and
append the following line containing the full path obtained earlier:

```
export PATH=$PATH:/home/dev/Tail
```

Then enter:

```
source ~/.bashrc
```

Close and reopen the terminal. The program may now be run from any directory.

## Usage

This program is intended to be used exactly as one would use the UNIX Tail 
program. From the Command Line Interface, invoke the program and specify the 
file to be be tailed. The last 10 lines of the file will be printed.

```
tail.py path/to/file.txt
```

To print a different number of lines, use the `-n` option followed by the 
number of lines you wish to print:

```
tail.py file.txt -n 5
```

Multiple files may be specified, in which case their tails will be preceded by 
a header indicating the file being printed:

```
tail.py file_1.txt file_2.txt file_3.txt
```

Files may be followed with the `-f` option such that the program will remain 
active and print any new data appended to the file being followed (multiple 
files may also be followed simultaneously). This is useful for monitoring
new entries of a log file as they are added:

> Note: To end the program after the follow option is specified, use the Ctrl+C
command to send an interrupt signal.

```
tail.py file.txt -f
```

To see a list of all arguments, specify the `-h` option

```
tail.py -h
```

## Limitations

The 'follow' option does not currently support rotating logs.

## License
MIT License

Copyright (c) 2021 nickelsr

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
