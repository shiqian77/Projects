#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 17:09:46 2021

@author: shiqianxu
"""

class Bear(object):
    '''
    define the bear's coordinate and direction, set the sleep turn of bear to zero
    '''
    def __init__(self,row,column,direction):
        self.r = row
        self.c = column
        self.d = direction
        self.sleep_turn = 0
        
    '''
    when the bear moves, its coordinate changes, save the change to the bear's coordinate
    '''
    def move(self):
        if self.d == 'N':
            self.r -= 1
        if self.d == 'S':
            self.r += 1
        if self.d == 'W':
            self.c -= 1
        if self.d == 'E':
            self.c += 1
        if self.d == 'NE':
            self.r -= 1
            self.c += 1
        if self.d == 'NW':
            self.r -= 1
            self.c -= 1
        if self.d == 'SE':
            self.r += 1
            self.c += 1
        if self.d == 'SW':
            self.r += 1
            self.c -= 1
            

    def goto_sleep(self, turns_to_sleep):
        self.sleep_turn = turns_to_sleep
        
    '''
    if the bear is asleep
    '''
    def sleep_round(self):
        if self.sleep_turn > 0:
            self.sleep_turn -= 1
            return True
        return False
    
    '''
    get coordinate of the bear
    '''
    def get_position(self):
        return (self.r,self.c)
    
    '''
    Note: this function is for part 1, didn't get used in part 2 and 3
    '''

    def __str__(self):
        p = 'Bear at ({},{}) moving {}\n'.format(str(self.r),str(self.c),str(self.d))
        return p
    
