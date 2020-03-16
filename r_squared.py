# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 17:08:37 2019

@author: peter
"""

import numpy as np

def r_squared(y, estimated):
    """
    Input
    list, y, that represents the y-coordinates of the original data samples
    estimated, which is a corresponding list of y-coordinates estimated from the regression model
    Return 
    the computed R^2 value. 
    You can compute R^2 as follows, 
    where ei is the estimated y value for the i-th data point (i.e. predicted by the regression), 
    yi is the y value for the ith data point, and mean is the mean of the original data samples. 
    """
   
    y_coordinates,           = np.array(y), 
    y_coordinates_estimated  = np.array(estimated)
    
    
    var_res = (((y_coordinates_estimated - y_coordinates)**2).sum())
    mean_original_data_samples = (y_coordinates.sum() / float(len(y_coordinates)))
    var_tot = ((mean_original_data_samples - y_coordinates)**2).sum()
    
    return ( 1 - var_res / var_tot )