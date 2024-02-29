#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 20:07:37 2021

@author: shiqianxu
"""

import json
from Bear import Bear
from Tourist import Tourist
from BerryField import Berryfield
'''
read the file, call the function to to print the result
'''
if __name__ == '__main__':
    file = input('Enter the json file name for the simulation => ')
    print(file)
    f = open(file)
    # f = open("bears_and_berries_1.json")
    data = json.loads(f.read())
    print('\nStarting Configuration')
    a = Berryfield(data['berry_field'], data['active_bears'], data['active_tourists'],data['reserve_bears'],data['reserve_tourists'])
    # print('')
    print(a)
    print('Active Bears:')

    for x in data['active_bears']:
        print('Bear at ({},{}) moving {}'.format(x[0],x[1],x[2]))
    print('\nActive Tourists:')
    for x in data['active_tourists']:
        print('Tourist at ({},{}), 0 turns without seeing a bear.'.format(x[0],x[1]))
    a.print_res()