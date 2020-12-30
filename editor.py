# editor.py
# A simple text editor built with Python curses standard library.
# https://wasimlorgat.com/editor

import argparse
import curses
import sys

def main(stdscr):
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    
    with open(args.filename) as f:
        buffer = f.readlines()
    
    while True:
        stdscr.erase()
        for row, line in enumerate(buffer):
            stdscr.addstr(row, 0, line)

        k = stdscr.getkey()
        if k == "q":
            sys.exit(0)
        
if __name__ == "__main__":
    curses.wrapper(main)