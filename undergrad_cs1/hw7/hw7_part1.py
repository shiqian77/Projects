#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 10:57:01 2021

@author: shiqianxu
"""

import string

'''determine if the word is in frenquency dictionary (dic) I created'''
def found(word,dic):
    if word in dic:
        return True
    else:
        return False

'''print the output'''
def print_found(word,dic,keyboard):
    if found(word,dic)==True:
        print('{}{} -> FOUND'.format(' '*(15-len(word)),word))
    if found(word,dic)==False:
        '''call the functions'''
        drop_w=drop(word)
        insert_w=insert(word)
        swap_w=swap(word)
        replace_w=replace(word,keyboard)
        ct=append(insert_w,replace_w,swap_w,drop_w)
        '''sort the big total list'''
        ct.sort(reverse =True)
        if ct==[]:
            print('{}{} -> NOT FOUND'.format(' '*(15-len(word)),word))
        if len(ct)==1:
            print('{}{} -> FOUND{}{}:  {}'.format(' '*(15-len(word)),word,' '* 2,len(ct),ct[0][1]))
        if len(ct)==2:
            print('{}{} -> FOUND{}{}:  {} {}'.format(' '*(15-len(word)),word,' '* 2,len(ct),ct[0][1],ct[1][1]))
        if len(ct)>=3:
            print('{}{} -> FOUND{}{}:  {} {} {}'.format(' '*(15-len(word)),word,' '* (3-len(str(len(ct)))),len(ct),ct[0][1],ct[1][1],ct[2][1]))

'''drop a letter from any position in the word, and you will get a new word, see if the new word is in dic and if it's not in the empty list, append the tuple(frequency,new word) to the empty list'''
def drop(word):
    correction_c1=[]
    for x in range(len(word)):
        new=word[:x] + word[x+1:]
        if found(new, dic)==True:
            if new not in correction_c1:
                correction_c1.append((dic[new],new))
    correction_c1 = set(correction_c1)
    correction_c1 = list(correction_c1)
    return correction_c1

'''append all the candidates lists to a big empty list'''
def append(correction_c1,correction_c2,correction_c3,correction_c4):
    correction_total=[]
    for x in correction_c1:
        correction_total.append(x)
    for x in correction_c2:
        correction_total.append(x)
    for x in correction_c3:
        correction_total.append(x)
    for x in correction_c4:
        correction_total.append(x)
    return correction_total

'''add a letter(go through a to z) to any position in the word, and you will get a new word, see if the new word is in dic and if it's not in the empty list, append the tuple(frequency,new word) to the empty list'''
def insert(word):
    correction_c2=[]
    a=string.ascii_lowercase
    for x in range(len(word)+1):
        for b in a:
            new=word[0:x] + b + word[x:]   
            if found(new, dic)==True:
                if new not in correction_c2:
                    freq=(dic[new],new)
                    correction_c2.append(freq)
    return correction_c2

'''change the position of two consecutive letters from the word from any position of the word, and you will get a new word, see if the new word is in dic and if it's not in the empty list, append the tuple(frequency,new word) to the empty list'''
def swap(word):
    correction_c3=[]
    for x in range(len(word) - 1):
        attempt = word[:x] + word[x+1] + word [x] + word[x+2:]
        if found(attempt, dic)==True:
            if attempt not in correction_c3:
                correction_c3.append((dic[attempt],attempt))
    return correction_c3 

'''replace a letter from the keyboard keys with the letters in keyboard values from any position of the word, and you will get a new word, see if the new word is in dic and if it's not in the empty list, append the tuple(frequency,new word) to the empty list'''
def replace(word,keyboard):
    correction_c4=[]
    for i in range(len(word)):
        letter = word[i]
        # print(letter)
        replace_list = keyboard[letter]
        for replacement in replace_list:
            attempt_word = word[:i] + replacement + word[i+1:]
            if found(attempt_word, dic) == True:
                if attempt_word not in correction_c4:
                    correction_c4.append((dic[attempt_word],attempt_word))
    return correction_c4


if __name__ == "__main__":
    '''input'''
    dfile=input('Dictionary file => ')
    # dfile="words_10percent.txt"
    print(dfile)
    ifile=input('Input file => ') # words_10percent.txt
    # ifile="input_words.txt"
    print(ifile)
    kfile=input('Keyboard file => ')
    # kfile="keyboard.txt"
    print(kfile)
    '''change the file to a dictionary with key of word, value of frequency'''
    dic = dict()
    for x in open(dfile, encoding = 'utf-8'):
        x=x.split(',')
        word=x[0]
        frequency=x[1].rstrip()
        dic[word]=frequency
    '''change the file to a dictionary with key of the first letter , value of the rest of letters'''
    keyboard=dict()
    for x in open(kfile,encoding = 'utf-8'):
        x=x.rstrip().split(' ')
        replace_letter=x[0]
        l=[]
        for y in range(1,len(x)):
            l.append(x[y])
        keyboard[replace_letter]=l
    '''go through each word in the input file'''
    f = open(ifile, encoding = 'utf-8')
    for x in f.readlines():
        x=x.rstrip()
        print_found(x,dic,keyboard)

