#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 19:20:48 2021

@author: shiqianxu
"""
from Bear import Bear
from Tourist import Tourist
import math
from copy import deepcopy


class Berryfield(object):
    '''
    create lists of bear object, tourist object, reserve bear object, reserve tourist object

    Note: only need lists of bear object, tourist object for hw part 1 and 2.
    
    '''
    def __init__(self, grid, bears, tourists, reserve_bears, reserve_tourists):
        self.berrygrid = grid
        bearsp = []
        for x in bears:
            bearsp.append(Bear(x[0], x[1], x[2]))
        self.b = bearsp
        touristsp = []
        for x in tourists:
            touristsp.append(Tourist(x[0],x[1]))
        self.t = touristsp
        reservebp = []
        for x in reserve_bears:
            reservebp.append(Bear(x[0], x[1], x[2]))
        self.rbp = reservebp
        reservetp = []
        for x in reserve_tourists:
            reservetp.append(Tourist(x[0],x[1]))
        self.rtp = reservetp

    '''
    record the sum of the berries and print the berryfield, and update it each time when changes occurs
    1.If there is a bear and tourist at the same spot, print 'X' at this spot.
    2.If there is a bear at the spot, print 'B' at this spot.
    3.If there is a tourist at the spot, print 'T' at this spot.
    '''
    def __str__(self):
        summ = 0
        for i in self.berrygrid:
            for j in i:
                summ += j
        print('Field has {} berries.'.format(summ))
        print_grid = deepcopy(self.berrygrid)
        field = ''
        for x in range(len(print_grid)):
            for y in range(len(print_grid[x])):
                for bear in self.b:
                    if bear.get_position() == (x,y):
                        print_grid[x][y] = 'B'
                        for tourist in self.t:
                            if tourist.get_position() == bear.get_position():
                                print_grid[x][y] = 'X'
                for tourist in self.t:
                    if print_grid[x][y] != 'X' and tourist.get_position() == (x,y):
                        print_grid[x][y] = 'T'
                field += '{:>4}'.format(str(print_grid[x][y]))
            field +='\n'
        return field

    '''
    If 1 <= # of berries < 10, it grows 1 berry at that spot
    '''
    def grow(self):
        for x in range(len(self.berrygrid)):
            for y in range(len(self.berrygrid[x])):
                if 1 <= int(self.berrygrid[x][y]) < 10:
                    self.berrygrid[x][y] += 1

    '''
    Get the coordinates of neighbour of the spot, append them to a list
    '''
    def berry_neighbour(self, x, y):
        bn = []
        if x + 1 == len(self.berrygrid):
            if y + 1 == len(self.berrygrid[x]):
                n1 = (x - 1, y)
                n2 = (x, y - 1)
                n3 = (x - 1, y - 1)
                bn.append(n1)
                bn.append(n2)
                bn.append(n3)
            if 0 < y < len(self.berrygrid[x]) - 1:
                n1 = (x - 1, y)
                n2 = (x, y + 1)
                n3 = (x, y - 1)
                n4 = (x - 1, y - 1)
                n5 = (x - 1, y + 1)
                bn.append(n1)
                bn.append(n2)
                bn.append(n3)
                bn.append(n4)
                bn.append(n5)
            if y == 0:
                n1 = (x, y + 1)
                n2 = (x - 1, y)
                n3 = (x - 1, y + 1)
                bn.append(n1)
                bn.append(n2)
                bn.append(n3)

        if x == 0:
            if y + 1 == len(self.berrygrid[x]):
                n1 = (x + 1, y)
                n2 = (x, y - 1)
                n3 = (x + 1, y - 1)
                bn.append(n1)
                bn.append(n2)
                bn.append(n3)
            if 0 < y < len(self.berrygrid[x]) - 1:
                n1 = (x, y - 1)
                n2 = (x, y + 1)
                n3 = (x + 1, y)
                n4 = (x + 1, y - 1)
                n5 = (x + 1, y + 1)
                bn.append(n1)
                bn.append(n2)
                bn.append(n3)
                bn.append(n4)
                bn.append(n5)
            if y == 0:
                n1 = (x, y + 1)
                n2 = (x + 1, y)
                n3 = (x + 1, y + 1)
                bn.append(n1)
                bn.append(n2)
                bn.append(n3)

        if 0 < x < len(self.berrygrid) - 1:
            if y + 1 == len(self.berrygrid[x]):
                n1 = (x - 1, y)
                n2 = (x + 1, y)
                n3 = (x, y - 1)
                n4 = (x - 1, y - 1)
                n5 = (x + 1, y - 1)
                bn.append(n1)
                bn.append(n2)
                bn.append(n3)
                bn.append(n4)
                bn.append(n5)
            if 0 < y < len(self.berrygrid[x]) - 1:
                n1 = (x - 1, y)
                n2 = (x + 1, y)
                n3 = (x, y - 1)
                n4 = (x, y + 1)
                n5 = (x - 1, y - 1)
                n6 = (x - 1, y + 1)
                n7 = (x + 1, y - 1)
                n8 = (x + 1, y + 1)
                bn.append(n1)
                bn.append(n2)
                bn.append(n3)
                bn.append(n4)
                bn.append(n5)
                bn.append(n6)
                bn.append(n7)
                bn.append(n8)
            if y == 0:
                n1 = (x -1 , y)
                n2 = (x + 1, y)
                n3 = (x, y + 1)
                n4 = (x - 1, y + 1)
                n5 = (x + 1, y + 1)
                bn.append(n1)
                bn.append(n2)
                bn.append(n3)
                bn.append(n4)
                bn.append(n5)
        return bn

    '''
    If any of the spot's neighbour has berry amount of 10, it grows 1 berry at that spot
    '''
    def spread(self):
        for x in range(len(self.berrygrid)):
            for y in range(len(self.berrygrid[x])):
                if self.berrygrid[x][y] == 0:
                    for (nx,ny) in self.berry_neighbour(x,y):
                        # print(nx,ny, "self:",x,y)
                        if self.berrygrid[nx][ny] == 10:
                            self.berrygrid[x][y] = 1
                            break

    '''
    check if the bear is inside the field(if the bear is out of boundary)
    '''
    def valid_bear_loc(self, bear):
        return (0 <= bear.r < len(self.berrygrid) and 0 <= bear.c < len(self.berrygrid[0]))

    """
    Updates all bear's location, and returns tourits that are in the way of the bears, the bear falls asleep for 3 turns when encounter the tourist
    """
    def bear_move(self):
        
        tourist_left = set()
        for bear in self.b:
            if bear.sleep_round():
                continue
            berry_bear_eat = 0
            while berry_bear_eat < 30 and self.valid_bear_loc(bear):
                meet_tourist = False
                for tour in self.t:
                    if (bear.r, bear.c) == tour.get_position():
                        tourist_left.add(tour)
                        meet_tourist = True
                if meet_tourist:
                    bear.goto_sleep(2)
                    break
                else:
                    eaten = min(30 - berry_bear_eat, self.berrygrid[bear.r][bear.c])
                    berry_bear_eat += eaten
                    self.berrygrid[bear.r][bear.c] -= eaten
                    if berry_bear_eat < 30:
                        bear.move()
        for tour in tourist_left:
            self.t.remove(tour)
        return tourist_left
    
    '''
    get the coordinates of the spots that are within 4 distance of the tourist's spot, add them to a dictionary
    '''
    def tourist_see_bears(self):
        tourist_box = dict()
        for x in range(len(self.berrygrid)):
            for y in range(len(self.berrygrid[x])):
                for i in self.t:
                    if math.sqrt((x - i.get_position()[0]) ** 2 + (y - i.get_position()[1]) ** 2) <= 4:
                        if i not in tourist_box:
                            tourist_box[i] = [(x,y)]
                        else:
                            tourist_box[i].append((x,y))
        return tourist_box
    
    """
    Find tourists that:
        1. Seen 3 bears around them, tourist get scared and leave, save the location of the tourist in a list
        2. Never seen any bears in 3 turns, tourist get bored and leave, save the location of the tourist in a list
    And, update the number of turns tourists have not seen any bear
        
    Note: 
        Those that are runed into bears are found by bear_move func above
    """
    def tourist_leave(self):

        tourist_box = self.tourist_see_bears()
        
        for tour in self.t:
            tour.increment_turn()
        
        tourist_scared = []
        
        for (tour, box) in tourist_box.items():
            number_bear_nearby = 0
            for b in self.b:
                if b.get_position() in box:
                    number_bear_nearby += 1
            if number_bear_nearby > 0:
                tour.seen_bear()
                
            if number_bear_nearby >= 3: # scared
                tourist_scared.append(tour)
                
        tourist_bored = []

        for tour in self.t:
            if tour.num_turn_no_bear >= 3:
                tourist_bored.append(tour)
                
        for tour in tourist_scared + tourist_bored:
            self.t.remove(tour)
            
        return tourist_scared, tourist_bored
    
    '''
    if the bear is not inside the field, the bear left, get the coordinates of the bear left the field, add them to a list
    '''
    def bear_leave(self):
        bear_outof_bound = []
        
        for bear in self.b:
            if not self.valid_bear_loc(bear):
                bear_outof_bound.append(bear)
                
        for bear in bear_outof_bound:
            self.b.remove(bear)
                
        return bear_outof_bound
    
    '''
    get the total number of berries
    
    Notes: this function is for hw part 3
    '''
    def get_total_berries(self):
        summ = 0
        for i in self.berrygrid:
            for j in i:
                summ += j
        return summ
    '''
    1.when there's still bears in the reserve queue and total number of berries is >= 500, the next reserve bear enter the field.
    2.when there's still tourists in the reserve queue and there's at least one active bear in the field, the next reserve tourist enter the field.
    
    Notes: this function is for hw part 3
    '''
    def reserve_enterfield(self):
        re_bear = []
        re_tourist = []
        if len(self.rbp) != 0 and self.get_total_berries() >= 500:
            first_re_bear = self.rbp[0]
            re_bear.append(first_re_bear)
            self.rbp.pop(0)
            self.b.append(first_re_bear)
            
        if len(self.rtp) != 0 and len(self.b) >= 1:
            first_re_tourist = self.rtp[0]
            re_tourist.append(first_re_tourist)
            self.rtp.pop(0)
            self.t.append(first_re_tourist)
        return re_bear, re_tourist

    '''
    print the result
    
    Notes:
        for hw part 1: print the original condition: before berry grows, bear moves, 
                       the berrygrid and its total number. active bear's coordinates 
                       and its moving direction, active tourist's coordinates 
        for hw part 2: print the result after the berry grows and bear moves, print 5 turns
        for hw part 3: print the result after the berry grows, bear moves, the reserve bear 
                       and reserve tourist enter the field. It runs till there are no bears 
                       in the field and no bears in the reserve queue or there are no bears 
                       in the field and there's no berries. It print the grid and active bear 
                       and tourists imformation every 5 turns and the last turn.
    '''


    def print_res(self):

        turn = 1

        while not(len(self.b) == 0 and len(self.rbp) == 0) or (len(self.b) == 0 and self.get_total_berries() == 0):
            # print(len(self.b))
            # print(len(self.rbp))
            # print(self.get_total_berries())
            self.grow()
            self.spread()
            tourist_get_eaten = self.bear_move()
            tourist_scared, tourist_bored = self.tourist_leave()
            
            bear_outof_bound = self.bear_leave()
            re_bear, re_tourist = self.reserve_enterfield()
            if turn == 1:
                print("\nTurn:", turn)
            else:
                print("\n\nTurn:", turn)
            for bear in bear_outof_bound:
                print('Bear at ({},{}) moving {} - Left the Field'.format(bear.get_position()[0], bear.get_position()[1], bear.d))

            
            for tour in tourist_get_eaten:
                print('Tourist at ({},{}), {} turns without seeing a bear. - Left the Field'.format(tour.get_position()[0], tour.get_position()[1], tour.num_turn_no_bear))

            for tour in tourist_bored:
                print('Tourist at ({},{}), {} turns without seeing a bear. - Left the Field'.format(tour.get_position()[0], tour.get_position()[1], tour.num_turn_no_bear))
            for tour in tourist_scared:
                print('Tourist at ({},{}), {} turns without seeing a bear. - Left the Field'.format(tour.get_position()[0], tour.get_position()[1], tour.num_turn_no_bear))

            for bear in re_bear:
                print('Bear at ({},{}) moving {} - Entered the Field'.format(bear.get_position()[0], bear.get_position()[1], bear.d))
            for tour in re_tourist:
                print('Tourist at ({},{}), 0 turns without seeing a bear. - Entered the Field'.format(tour.get_position()[0], tour.get_position()[1]))

            if turn % 5 == 0:
                print(str(self))
                print('Active Bears:')
                for bear in self.b:
                    if bear.sleep_turn == 0:
                        print('Bear at ({},{}) moving {}'.format(bear.get_position()[0], bear.get_position()[1], bear.d))
                    else:
                        print('Bear at ({},{}) moving {} - Asleep for {} more turns'.format(bear.get_position()[0], bear.get_position()[1], bear.d, bear.sleep_turn))
                print('')
                print('Active Tourists:')
                for tour in self.t:
                    print('Tourist at ({},{}), {} turns without seeing a bear.'.format(tour.get_position()[0], tour.get_position()[1], tour.num_turn_no_bear))
            turn += 1
        print()
        print(str(self))
        print('Active Bears:')
        for bear in self.b:
            if bear.sleep_turn == 0:
                print('Bear at ({},{}) moving {}'.format(bear.get_position()[0], bear.get_position()[1], bear.d))
            else:
                print('Bear at ({},{}) moving {} - Asleep for {} more turns'.format(bear.get_position()[0], bear.get_position()[1], bear.d, bear.sleep_turn))
        print('')
        print('Active Tourists:')
        for tour in self.t:
            print('Tourist at ({},{}), {} turns without seeing a bear.'.format(tour.get_position()[0], tour.get_position()[1], tour.num_turn_no_bear))

        return turn
