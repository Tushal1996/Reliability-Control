#! /usr/bin/env python
# -*- coding:utf-8 -*-


'''
Created on 01.09.1009

@author: reqnik
'''
import numpy as np

class B_transformation():
    # @reqnik: Explaination? 
    def __init__(self, parameters):
        self._parameters=parameters
    
    def calcTI(self,windspeed,B_value):
        TI = (self._parameters[0] + windspeed * self._parameters[1] + self._parameters[2] * B_value + self._parameters[3] * windspeed * B_value) / windspeed
        return TI
    
    def calcB(self,windspeed,TI):
        B_value = (TI * windspeed - (self._parameters[0] + windspeed * self._parameters[1])) / (self._parameters[2] + windspeed * self._parameters[3])
        return B_value
    
    def calcSTD(self,windspeed,B_value):
        TI = (self._parameters[0] + windspeed * self._parameters[1] + self._parameters[2] * B_value + self._parameters[3] * windspeed * B_value)
        # @reqnik: function name says calcSTD but the return variable is TI?
        return TI
    
    def calcBFromSTD(self,windspeed,stdVal):
        B_value = (stdVal - (self._parameters[0] + windspeed * self._parameters[1])) / (self._parameters[2] + windspeed * self._parameters[3])
        return B_value
    


def get_interpolation(ranges, a, p):
    # @reqnik: is this a general interpolation function? What is a, what is p?
    for i in range(a.ndim):
        # check if we are out of range, if yes than use the last bounded values
        if p[i] <= ranges[i][0]:
            a = a[0]
            continue
        if p[i] >= ranges[i][-1]:
            a = a[-1]
            continue

        # find the nearest values
        right = np.searchsorted(ranges[i], p[i])
        left = right - 1

        # find the relative distance
        d = (p[i] - ranges[i][left]) / (ranges[i][right] - ranges[i][left])

        # calculate the interpolation
        a = (1 - d) * a[left] + d * a[right]
        # print('Interpolation: ', a)

    return a

