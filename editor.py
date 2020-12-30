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

class Cursor:
    def __init__(self, row=0, col=0, col_hint=None):
        self.row = row
        self._col = col
        self._col_hint = col if col_hint is None else col_hint
    
    @property
    def col(self):
        return self._col
    
    @col.setter
    def col(self, col):
        self._col = col
        self._col_hint = col
    
    def up(self, buffer):
        if self.row > 0:
            self.row -= 1
            self._clamp_col(buffer)
        
    def down(self, buffer):
        if self.row < len(buffer) - 1:
            self.row += 1
            self._clamp_col(buffer)
        
    def right(self, buffer):
        if self.col < len(buffer[self.row]) - 1:
            self.col += 1
        
    def left(self):
        if self.col > 0:
            self.col -= 1
            
    def _clamp_col(self, buffer):
        self._col = min(self._col_hint, len(buffer[self.row]))

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
        stdscr.move(cursor.row, cursor.col)

        k = stdscr.getkey()
        if k == "q":
            sys.exit(0)
        elif k == "KEY_UP":
            cursor.up(buffer)
        elif k == "KEY_DOWN":
            cursor.down(buffer)
        elif k == "KEY_RIGHT":
            cursor.right(buffer)
        elif k == "KEY_LEFT":
            cursor.left()
        
if __name__ == "__main__":
    curses.wrapper(main)