#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 00:35:50 2021

@author: shiqianxu
"""
import json
from bear import Bear
from tourist import Tourist
from berryfield import Berryfield
'''
read the file, call the function to to print the result, all the comments are in every file in part 3 
'''
if __name__ == '__main__':
    file = input('Enter the json file name for the simulation => ')
    print(file)
    f = open(file)
    # f = open("bears_and_berries_1.json")
    data = json.loads(f.read())
    a = Berryfield(data['berry_field'], data['active_bears'], data['active_tourists'])
    print('')
    print(a,end = '')

    