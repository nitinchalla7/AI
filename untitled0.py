# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 08:45:10 2020

@author: Nitin Challa
"""

import random

#---------DARES--------

dare_items  = ['dance in the street like crazy.', 'Bark like a dog loudly.', 'take your shirt off and spin it.']

#---------------------------------------


times_gonna_play = input('please tell me how many times you want to play?')
times_gonna_play = int(times_gonna_play)

for i in range(times_gonna_play) :
    
    print('The dares are: ')
    dares = random.sample(dare_items, 2)
    print('Dare 1 --> ' + dares[0])
    print('Dare 2 --> ' + dares[1])
    p1 = input('please type player 1 name   ')
    p2 = input('please type player 2 name   ')
    
    p1 = str(p1)
    p2 = str(p2)  
    
    
    players = []
    players.append(p1)
    players.append(p2)
    
    pChoice = random.sample(players, 2)
    
    
    input("Press Enter to see the dares..")
    print(pChoice[0] + ': ' + dares[0])
    print(pChoice[1] + ': ' + dares[1])
    