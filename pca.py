# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 21:17:19 2020

@author: Nitin Challa
"""
from scipy.io import loadmat
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def load_and_center_dataset(filename):
    dataset = loadmat(filename) #load the file
    x = np.array(dataset['fea'])
    n = len(x)
    d = len(x[0])
    x = np.array([], dtype = float)

    return x - np.mean(x, axis=0) #center the image data

# calculate and return the covariance matrix of the dataset as a NumPy matrix
# (d x d array)
def get_covariance(dataset):
    n = len(dataset)
    const = 1/(n - 1)
    cov = [] 
    cov = np.dot(np.transpose(dataset), dataset) * const #using the formula calculate the covariance

    return cov

def get_eig(S, m):
    w, v = eigh(S)
    w = w[-m:] #flip the diagonal
    w = np.flip(w, axis=0)
    v = np.transpose(v)
    v = v[-m:] #flip the eigenvector array
    v = np.flip(v, axis=0)
    v = v.T
    
    ev = np.identity(m, dtype=float)
    return np.multiply(w, ev), v

def project_image(image,U):
    x = np.dot(image,U)
    x = np.dot(x,np.array(U).transpose()) #use with eigenvectors to create a projection of the image
    return x

def display_image(orig, proj):
    orig2 = orig.thumbnail((32, 32), Image.ANTIALIAS)
    proj2 = proj.thumbnail((32, 32), Image.ANTIALIAS)   #resize the images to 32x32
    fig = plt.figure()
    a = fig.add_subplot(1, 2, 1) #create a row of subplots to add the images to
    imgplot = plt.imshow(orig2)
    a.set_title('Original')
    plt.colorbar(ticks=[-25, 0, 25, 50, 75, 100, 125], orientation='vertical')
    a = fig.add_subplot(1, 2, 2)
    imgplot = plt.imshow(proj2)
    a.set_title('Projection') #set titles for each subplot
    plt.colorbar(ticks=[20, 40, 60, 80], orientation='vertical') #create the color bar
    plt.imshow(aspect='equal') #set aspect to the same for both
    plt.show() #show the images