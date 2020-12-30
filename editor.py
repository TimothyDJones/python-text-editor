# editor.py
# A simple text editor built with Python curses standard library.
# https://wasimlorgat.com/editor

import curses
import sys

def main(stdscr):
    while True:
        k = stdscr.getkey()
        if k == "q":
            sys.exit()
        
if __name__ == "__main__":
    curses.wrapper(main)