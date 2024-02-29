#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 16:45:11 2021

@author: shiqianxu
"""
import json

def find_year(movies,maxy,miny):
    m1 = []
    for x in movies:
        if miny <= movies[x]['movie_year'] and movies[x]['movie_year']<= maxy:
            m1.append(movies)
    return m1



if __name__ == "__main__":
    movies = json.loads(open("movies.json").read())
    ratings = json.loads(open("ratings.json").read())
    min_y = input("Min year => ")
    print(min_y)
    min_y = int(min_y)
    max_y = input("Max year => ")
    print(max_y)
    max_y = int(max_y)
    m1 = find_year(movies, max_y, min_y)
    print(m1)
