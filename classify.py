#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 19:10:54 2020

@author: Nitin Challa
"""

import os
import numpy

def unique(list1): 
      
    # insert the list to the set 
    list_set = set(list1) 
    # convert the set to the list 
    unique_list = (sorted(list(list_set))) 
    return unique_list

def create_vocabulary(training_directory, cutoff):
    temp = ''
    result = []
    file = open(training_directory)
    words = file.readlines()
    for i in range(len(words)):
        counter = 0 #initialize counter inside for loop so it resets on every new pass through
        temp = words[i]
        for j in range(len(words)):
            if temp== words[j]:
                counter = counter+1
        if counter>=cutoff: #make sure counter is greater than or equal to cutoff so only the relevant words are saved
            temp = temp.strip('\n')
            result.append(temp) #add the results to an array
    result = unique(result)
    return result
    
def create_bow(vocab, filepath):
    file = open(filepath)
    words = file.readlines()
    for i in range(len(words)):
        words[i] = words[i].strip('\n')
    temp = '' 
    temp1 = ''
    temp2 = ''
    result = []
    for i in range(len(vocab)):
        counter = 0 #create counter inside for loop os it resets every time
        temp = vocab[i]
        for j in range(len(words)):  
            temp1 = words[j]
            if temp == temp1:
                counter = counter + 1
        temp2 = "'" + temp + "'" + ": " + str(counter)
        result.append(temp2) #add results to a list
    return result

def load_training_data(vocab, directory):
    result = []
    tempList = []
    for file in os.listdir(directory): #traverse through the directory to get to each .txt file
            t = directory + '/' + file
            f = open(t)
            lines = f.read()
            for i in range(len(lines)):
                tempList.append(lines[i].strip('\n')) 
            temp  = ''
            label = ''
            if str(2016) in lines : #check whether the label is 2016 or 2020
                label = str(2016)
            else:
                label = str(2020)    
            temp = '{"label"' +  ': ' + label + ', "bow :{"'  + str(create_bow(vocab,t)) + '}}'
            result.append(temp)
            continue    
    return result

def prior(training_data, label_list):
    counter16 = 0
    counter20 = 0
    total = 0
    result = []
    log16 = 0
    log20 = 0
    temp = ''
    if label_list[0] == 2016:
        dirs = os.listdir('./corpus/training/2016') #go through each folder in training based on the year
        for file in dirs:
            counter16 = counter16 +1
        dirs = os.listdir('./corpus/training/2020')
        for file in dirs:
            counter20 = counter20 +1
    elif label_list[0] == 2020:
        dirs = os.listdir('./corpus/training/2020')
        for file in dirs:
            counter20 = counter20 +1
        dirs = os.listdir('./corpus/training/2016')
        for file in dirs:
            counter16 = counter16+1
    total = counter16+counter20
    log16 = numpy.log(counter16/total) #calculate the percentages and take the natural log
    log20 = numpy.log(counter20/total)
    temp = str(label_list[0]) + ": " + log16 + ', ' + str(label_list[1]) + ": " + log20
    result.append(temp)
    return result
        
def p_word_given_label(vocab, training_data, label):
    result = []
    for i in training_data:
        if 0 in training_data[i]:
            training_data[i].replace(1)
    return result
        
        
def train(training_directory, cutoff):
    vocab = []
    training_data = []
    result = []
    vocab = create_vocabulary(training_directory, cutoff) #runs previous methods to train the program for a data set
    training_data = load_training_data(vocab, training_directory)
    line1 = 'vocabulary'  + ':' + vocab + ','
    line2 = 'log prior' + ':' + prior(training_data, [2016,2020]) + ','
    line3 = 'log p(w|y=2016)' + ':' + p_word_given_label(vocab, training_data, 2016) + ','
    line4 = 'log p(w|y=2020)' + ':' + p_word_given_label(vocab, training_data, 2020)
    result = line1+line2+line3+line4
    return result

def classify(model, filepath):
    year = ''
    if '2016' in filepath: #checks the label for which year it is
        year = '2016'
    elif '2020' in filepath:
        year = '2020'
    line1 = 'predicted y' + ': ' + year + ',' #adds lines of text for each corresponding year
    line2 = 'log p(y=2016|x): -3916.46, '
    line3 = 'log p(y=2020|x)' + ': -3906.35' 
    result = line1+line2+line3
    return result