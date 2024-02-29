#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 14:23:40 2021

@author: shiqianxu
"""
import json
'''step1: put the movies dictionary to the first filter: if the movie year is inside the year range, add the corresponding small dictionary to an empty dictionary m1'''
def find_year(movies,maxy,miny):
    m1 = dict()
    for x in movies:
        if miny <= movies[x]['movie_year'] and movies[x]['movie_year']<= maxy:
            m1[x] = movies[x]
    return m1

'''step2: put the dictionary I get from last step to the second filter: if the length of the twitter rating is greater to three, append the key of the ratings dictionary to en empty list index. Add the small dictionary which has the ID number in index list to an empty dictionary m2. At the same time calculating the combined average rating, add the average key to the small dictionary'''
def cal_combined_rating(m1,ratings,wi,wt):
    r1 = dict()
    index = []
    for x in ratings:
        if len(ratings[x]) >= 3:
            r1[x] = ratings[x]
            index.append(x)

    m2 = dict()
    for x in m1:
        if x in index:
            m2[x] = m1[x]
    for x in m2:
        avg = wi * m2[x]['rating'] + wt * (sum(r1[x])/len(r1[x])) / (wi + wt)
        m2[x]['avg']=avg
    return m2

'''step3: put the dictionary I get from last step to the third filter:if the genre is in dictionary[id]['genre'],add the corresponding small dictionary to an empty dictionary m3'''
def find_genre(m2,genre):
    m3 = dict()
    for x in m2:
        if genre in m2[x]['genre']:
            m3[x] = m2[x]
    return m3

'''find the movie, movie's year,best rating'''
def best(m3):
    max1 = 0
    best = ""
    byear = 1000
    for x in m3:
        if (m3[x]['avg'] > max1) or \
                (m3[x]['avg'] == max1 and m3[x]['name'] > best):
            max1 = m3[x]['avg']
            best = m3[x]['name']
            byear = m3[x]['movie_year']
    return max1, best, byear

'''find the movie, movie's year,worst rating'''
def worst(m3):
    min1 = 10.0
    worst = ""
    for x in m3:
        if m3[x]['avg'] < min1 or \
                (m3[x]['avg'] == min1 and m3[x]['name'] > worst):
            min1 = m3[x]['avg']
            worst = m3[x]['name']
            wyear = m3[x]['movie_year']
    return min1, worst, wyear

def collect_genres(movies):
    genres = set()
    for x in movies:
         for genre in movies[x]['genre']:
             genres.add(genre)
    return genres

if __name__ == "__main__":
    '''change the two file into dictionary mode'''
    movies = json.loads(open("movies.json").read())
    ratings = json.loads(open("ratings.json").read())
    '''input'''
    min_y = input("Min year => ")
    print(min_y)
    min_y = int(min_y)
    max_y = input("Max year => ")
    print(max_y)
    max_y = int(max_y)
    wi = input("Weight for IMDB => ")
    print(wi)
    wi = float(wi)
    wt = input("Weight for Twitter => ")
    print(wt)
    print()
    wt = float(wt)
    '''call the fuctions'''
    m1 = find_year(movies, max_y, min_y)
    m2 = cal_combined_rating(m1, ratings, wi, wt)
    genres = collect_genres(m2)
    '''call the fuctions and print the output'''
    while True:
        genre = input('What genre do you want to see? ')
        print(genre)
        if genre.lower() == 'stop':
            break
        genre = genre.title()
        if genre not in genres:
            print('\nNo {} movie found in {} through {}\n'.format(genre,min_y,max_y))
            continue
        m3 = find_genre(m2, genre)
        best_rating, best_movie, best_year = best(m3)
        worst_rating, worst_movie, worst_year = worst(m3)
        print('\nBest:')
        print('{}Released in {}, {} has a rating of {:.2f}\n'.format(' '*8,best_year,best_movie,best_rating))
        print('Worst:')
        print('{}Released in {}, {} has a rating of {:.2f}\n'.format(' '*8,worst_year,worst_movie,worst_rating))
        







