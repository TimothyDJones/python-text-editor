# editor.py
# A simple text editor built with Python curses standard library.
# https://wasimlorgat.com/editor

import argparse
import curses
import sys

class Window:
    def __init__(self, n_rows, n_cols):
        self.n_rows = n_rows
        self.n_cols = n_cols

def Cursor:
    def __init__(self, row=0, col=0):
        self.row = row
        self.col = col

def main(stdscr):
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    
    with open(args.filename) as f:
        buffer = f.readlines()
    
    window = Window(curses.LINES - 1, curses.COLS - 1)
    cursor = Cursor()
    
    while True:
        stdscr.erase()
        for row, line in enumerate(buffer[:window.n_rows]):
            stdscr.addstr(row, 0, line[:window.n_cols])
        stdscr.move(cursor.line, cursor.col)

        k = stdscr.getkey()
        if k == "q":
            sys.exit(0)
        
if __name__ == "__main__":
    curses.wrapper(main)