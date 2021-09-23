#!/usr/bin/env python

import os
import sys
import argparse
import time
import signal
from threading import Thread, Lock, Event
from pathlib import Path


class Tail(object):
    """Prints tail-end of files and their subsequent updates.

    Class Vars:
    BLOCK_SIZE (int): number of bytes to read into memory simultaneously

    Instance Vars:
    n
    files
    _lock

    Methods:
    tails()
    followFile(file)
    _lastNLines(file)
    """

    BLOCK_SIZE = 8192

    def __init__(self, fnames, n):
        """Initialize Tail object.
        
        Parameters:
        fnames [string]: Names of files to be tailed
        n (int): Number of lines to print

        Instance Vars:
        files [File]: List of VALID File objects
        n (int): Number of lines to print
        _lock (threading.Lock): Threading Lock to ensure proper format of
                                output when multiple files are being followed
        """
        self.files = [f for f in [File(fn) for fn in fnames] if f.is_valid()]
        self.n = n
        self._lock = Lock()
    
    def get_files(self):
        """Returns files ([File])."""
        return self.files
    
    def get_n(self):
        """Returns n (int)."""
        return self.n

    def get_lock(self):
        """Returns _lock (threading.Lock)."""
        return self._lock

    def tails(self):
        """Print header and last N lines of file.
        
        Only print header if given multiple files to read.
        """
        for i, f in enumerate(self.files):
            if len(self.files) > 1: print(f"\n==> {f.get_filename()} <==")
            self._lastNLines(f)

    def _lastNLines(self, file):
        """Print last N lines of file and update filesize.

        Read in and output lines in BLOCK_SIZE blocks to limit memory use.
        Begin reading from end of file to reduce time complexity from
        O(sizeof(file)) to O(N) where N is number of lines to print.
        
        Parameters:
        file (File): File object to be read from
        """
        with open(file.get_filename(), "r") as f:
            newlines = 0
            pos = filesize = f.seek(0, os.SEEK_END)
            while pos > 0 and newlines < self.n + 1:
                if pos < Tail.BLOCK_SIZE: curr_block_size = pos
                else: curr_block_size = Tail.BLOCK_SIZE
                pos -= curr_block_size
                f.seek(pos)
                block = f.read(curr_block_size)
                newlines += block.count('\n')
                if newlines >= self.n + 1:
                    nlList = [i for i, c in enumerate(block) if c == '\n']
                    diff = self.n + 1 - newlines
                    offset = nlList[-diff] + 1
                    f.seek(pos + offset)
            if newlines < self.n + 1:
                f.seek(0)
            while (f.tell() < filesize):
                print(f.read(Tail.BLOCK_SIZE), end='')
            file.update_pos(filesize)

    def followFile(self, file):
        """Print new characters when file is appended to or overwritten.
        
        Parameters:
        file (File): File object to be read from
        """
        with self.get_lock():
            n = 1
            with open(file.get_filename(), "r") as f:
                curr_end = f.seek(0, os.SEEK_END)
                diff = curr_end - file.get_pos()
                if curr_end - file.get_pos() < 0:
                    print(f"{file.get_filename()}: file truncated")
                    f.seek(0)
                else:
                    f.seek(file.get_pos())
                if f.tell() < curr_end:
                    print(f"\n==> {file.get_filename()} <==")
                while f.tell() < curr_end:
                    print(f.read(Tail.BLOCK_SIZE), end='')
                file.update_pos(curr_end)


class Follower(Thread):
    """A Thread that executes its target function until interrupted."""
    def __init__(self, target, args):
        """

        Parameters:
        target (function): Function to be executed
        args (tuple): Arguments to pass to target function

        Instance vars:
        shutdown_flag (threading.Event): Flag to signal thread termination
        target (function): Function to be executed
        args (tuple): Arguments to pass to target function
        """
        Thread.__init__(self)
        self.shutdown_flag = Event()
        self.target = target
        self.args = args
    
    def run(self):
        """Execute target function until shutdown_flag signals termination."""
        while not self.shutdown_flag.is_set():
            self.target(*self.args)
            time.sleep(0.1)
    
    def shutdown(self):
        """Set shutdown_flag and terminate thread."""
        self.shutdown_flag.set()
        self.join()


class File(object):
    """Holds file information.
    
    Instance Vars:
    filename (string): Name of file
    pos (int): Byte position that last read ended on

    Methods:
    get_filename()
    get_pos()
    update_pos()
    is_valid()
    """

    def __init__(self, filename, pos=0):
        """Initialize File object."""
        self.filename = filename
        self.pos = pos

    def get_filename(self):
        """Returns filename (string)."""
        return self.filename
    
    def get_pos(self):
        """Returns position (int)."""
        return self.pos

    def update_pos(self, pos):
        """Updates position (int)."""
        self.pos = pos

    def is_valid(self):
        """Checks if file exists and is readable.
        
        Returns:
        Bool
        """
        file = Path(self.get_filename())
        if not file.exists():
            print(f"tail: cannot open '{self.get_filename()}': " +
                  "No such file or directory")
            return False
        if file.is_dir():
            print(f"tail: cannot open '{self.get_filename()}': " +
                  "Is a directory")
            return False
        return True


class ServiceExit(Exception):
    """For clean exit of follower threads"""
    pass


def signal_handler(signum, frame):
    raise ServiceExit

def main():
    parser = argparse.ArgumentParser(description='''Print the last 10 lines of
                                     each FILE to standard output. With more
                                     than one FILE, precede each with a header
                                     giving the file name.''')

    parser.add_argument("-n", "--lines", type=int, metavar="NUM",
                        help="output last NUM lines, instead of last 10")

    parser.add_argument("FILE", nargs=argparse.ONE_OR_MORE,
                        help="name of file")

    parser.add_argument("-f", "--follow", action="store_true",
                        help="output appended data as the file grows")

    args = parser.parse_args()
    if args.lines == None: args.lines = 10
    if args.lines < 0: args.lines = abs(args.lines)
    tail = Tail(args.FILE, args.lines)
    tail.tails()
    if not args.follow: return
    threads = []
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    try:
        for f in tail.get_files():
            follower = Follower(target=tail.followFile, args=(f,))
            threads.append(follower)
            follower.start()
        while True:
            time.sleep(0.1)
    except ServiceExit:
        for t in threads:
            t.shutdown()
        print()

if __name__ == '__main__':
    main()
