#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 17:10:03 2021

@author: shiqianxu
"""

class Tourist(object):
    '''
    define the bear's coordinate, and set the number of turn not see any bears to 0
    '''
    def __init__(self,row,column):
        self.r = row
        self.c = column
        self.num_turn_no_bear = 0
    
    '''
    get coordinate of tourist
    '''
    def get_position(self):
        return (self.r,self.c)

    def increment_turn(self):
        self.num_turn_no_bear += 1
    '''
    Once see a bear, number of turn not see any bears become 0 again
    '''
    def seen_bear(self):
        self.num_turn_no_bear = 0
        
    '''
    Note: this function is for part 1, didn't get used in part 2 and 3
    '''
    def __str__(self):
        s = 'Tourist at ({},{}), 0 turns without seeing a bear.\n'.format(str(self.r),str(self.c))
        return s