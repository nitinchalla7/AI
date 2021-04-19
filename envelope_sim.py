#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 17:32:59 2020

@author: Nitin Challa
"""

import random

def pick_envelope(switch, verbose):
    e0 = []
    e1 = []
    color = ''
    choice = []
    post = []
    e0 = random.sample(['r','b','b','b'], 2) #to pick two balls for first envelope
    
    if 'r' in e0:
        e1 = ['b','b'] #fill second envelope with black balls if the first one has red
    else:
        e1 = random.sample(['r','b'], 2) #if not then random sample to pick order of black and red ball
        
    temp = random.sample([e0, e1], 1)
    choice = temp[0]
    if choice == e0: #create a variable that stores the opposite of the current envelope so switching becomes easier
        post = e1
    else:
        post = e0
    if choice == e0:
        temp2 = random.sample([e0[0], e0[1]], 1)
        color = temp2[0]
    else:
        temp2 = random.sample([e1[0], e1[1]], 1)
        color = temp2[0]
    if verbose is True: #to print out the statements if verbose is true
        print('Envelope 0: ' + e0[0] + " " + e0[1])
        print('Envelope 1: ' + e1[0] + " " + e1[1])
        if choice == e0:
            print('I picked envelope 0')
        elif choice == e1:
            print('I picked envelope 1')
        if color == 'r':
            print('and drew a r')
            return(True)
            exit
        elif color == 'b':
            print('and drew a b')
        if switch is True:
            if post is e1:
                print('Switch to envelope 1')
            else:
                print('Switch to envelope 0')
        if (switch == True and ('r' in post)): #these are the winning cases
            return(True)
        elif (switch == False and ('r' in choice)):
            return(True)
        else:
            return(False)
    else:
        if color == 'r':
            return(True)
            exit
        if (switch == True and ('r' in post)):
            return(True)
        elif (switch == False and ('r' in choice)):
            return(True)
        else:
            return(False)

def run_simulation(n):
    i=0
    j=0
    counter=0
    counter2=0
    succ = 0
    succ2 = 0
    while(i<=n): #loop to keep testing cases and adding to the counter
        if pick_envelope(True, verbose=False) == True:
            counter = counter + 1
        i = i+1
    while(j<=n):
        if pick_envelope(False, verbose=False) is True:
            counter2 = counter2 + 1
        j = j+1
    succ = counter/n #find win percentage for switching
    succ2 = counter2/n #find win percentage for no switching
    print('After ' + str(n) + ' simulations:')
    print('  Switch successful: ' + str(succ*100) + '%')
    print('  No-switch successful: ' + str(succ2*100) + '%')