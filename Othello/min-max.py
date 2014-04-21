# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 12:11:14 2014

@author: pratool
"""

import Othello

def MinMax(board):
    return MaxMove(board)

def MaxMove(board):
    if terminal_test():
        