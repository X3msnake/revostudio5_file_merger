#! /usr/bin/env python3
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 7.6
#  in conjunction with Tcl version 8.6
#    May 25, 2023 01:31:49 AM BST  platform: Windows NT

import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *

import revostudio_mergeui

_debug = True # False to eliminate debug printing from callback functions.

def main(*args):
    '''Main entry point for the application.'''
    global root
    root = tk.Tk()
    root.protocol( 'WM_DELETE_WINDOW' , root.destroy)
    # Creates a toplevel widget.
    global _top1, _w1
    _top1 = root
    _w1 = revostudio_mergeui.Toplevel1(_top1)
    root.mainloop()

def add_main_file(*args):
    if _debug:
        print('revostudio_mergeui_support.add_main_file')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()

def add_merge_file(*args):
    if _debug:
        print('revostudio_mergeui_support.add_merge_file')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()

def merge_files(*args):
    if _debug:
        print('revostudio_mergeui_support.merge_files')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()

if __name__ == '__main__':
    revostudio_mergeui.start_up()




