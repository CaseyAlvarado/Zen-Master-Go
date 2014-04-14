# -*- coding: utf-8 -*-
"""
Created on Sun Apr 13 18:38:54 2014

@author: Pratool
"""

def check_for_list(branch):
    for item in branch:
        if type(item) == list:
            return True
    return False

def modified_min(in_list):
    minimum = 1000
    for element in in_list:
        if type(element) == tuple:
            if element[0] < minimum:
                minimum = element[0]
        elif element < minimum:
            minimum = element
    return minimum

def modified_max(in_list):
    maximum = -1000
    for element in in_list:
        if type(element) == tuple:
            if element[0] > maximum:
                maximum = element[0]
        elif element > maximum:
            maximum = element
    return maximum

def find_max_depth(in_list, current_depth):
    max_depth = current_depth
    for element in in_list:
        if type(element) == tuple:
            if element[1] > max_depth:
                max_depth = element[1]
    return max_depth

def flatten_tree(rec_tree, depth):
    if not(check_for_list(rec_tree)):   # if there are no lists in rec_tree
        if depth % 2 == 0:              # if it's computer's move
            return (modified_max(rec_tree), find_max_depth(rec_tree, depth))
        return (modified_min(rec_tree), find_max_depth(rec_tree, depth))
    else:
        branch = []
        for element in rec_tree:
            if type(element) == list:
                branch.append(flatten_tree(element, depth+1))
            else:
                branch.append(element)
        return flatten_tree(branch, depth)

print flatten_tree([1, 2, [5, 8, 6], [3, 8, 4], 6], 0)
print flatten_tree([1, 2, [5, 6, [1, 0, 4], 3]], 0)