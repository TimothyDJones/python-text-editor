# editor.py
# A simple text editor built with Python curses standard library.
# https://wasimlorgat.com/editor

import argparse
import curses
import sys

class Window:
    def __init__(self, n_rows, n_cols, row=0, col=0):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.row = row
        self.col = col
        
    @property
    def bottom(self):
        return self.row + self.n_rows - 1
    
    def up(self, cursor):
        if cursor.row == self.row - 1 and self.row > 0:
            self.row -= 1
            
    def down(self, buffer, cursor):
        if cursor.row == self.bottom + 1 and self.bottom:
            self.row += 1
    
    # Convert cursor position relative to window (instead of screen)
    def translate(self, cursor):
        return cursor.row - self.row, cursor.col - self.col

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
        elif self.row < len(buffer) - 1:
            self.row += 1
            self.col = 0
        
    def left(self, buffer):
        if self.col > 0:
            self.col -= 1
        elif self.row > 0:
            self.row -= 1
            self.col = len(buffer[self.row])
            
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
        for row, line in enumerate(buffer[window.row:window.n_rows]):
            stdscr.addstr(row, 0, line[:window.n_cols])
        stdscr.move(*window.translate(cursor))

        k = stdscr.getkey()
        if k == "q":
            sys.exit(0)
        elif k == "KEY_UP":
            cursor = cursor.up(buffer)
            window = window.up(cursor)
        elif k == "KEY_DOWN":
            cursor = cursor.down(buffer)
            window = window.down(buffer, cursor)
        elif k == "KEY_RIGHT":
            cursor = cursor.right(buffer)
            window = window.down(buffer, cursor)
        elif k == "KEY_LEFT":
            cursor = cursor.left(buffer)
            window = window.up(cursor)
        
if __name__ == "__main__":
    curses.wrapper(main)