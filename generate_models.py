# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 16:49:58 2019

@author: peter
"""

import numpy as np

def generate_models(x, y, degs):
    """
    
    x and y are two lists corresponding to the x-coordinates and y-coordinates of the data samples (or data points)
    degs is a list of integers indicating the degree of each regression model that we want to create
    return a list of models. A model is the numpy 1d array of the coefficients of the fitting polynomial curve
        
    """
    
    return ([np.polyfit(x, y, z) for z in degs])




print(generate_models([1961, 1962, 1963],[4.4,5.5,6.6],[1, 2]))



   