#! /usr/bin/env python
# -*- coding:utf-8 -*-

'''
Created on 02.09.2019

import scipy.interpolate
import scipy.integrate
import numpy as np
from Simulations import functions
import time

class BasicTurbine():
    def __init__(self, timeVec, inputDataArray, lookUpTableGridValues, lookUpTables):
        self._timeVec=timeVec
        self._dataArray=inputDataArray
        self._gridValues=lookUpTableGridValues
        self._lookUpTables = lookUpTables
        
        
    def interpolateAllValues(self):
        self._interpolatedValues={}
        for lookUpTableName in self._lookUpTables:
            interpolatedValues=scipy.interpolate.interpn(self._gridValues,self._lookUpTables[lookUpTableName],self._dataArray, bounds_error=False,fill_value=None)
            interpolatedValues[np.where(interpolatedValues<0)]=0
            self._interpolatedValues[lookUpTableName]=interpolatedValues

            
    def integrateInterpolatedValues_trapz(self):
        self._integratedValues={}
        for lookUpTableName in self._lookUpTables:
            self._integratedValues[lookUpTableName]=scipy.integrate.cumtrapz(self._interpolatedValues[lookUpTableName], initial=0)
            
    def integrateInterpolatedValues_sum(self):
        self._integratedValues={}
        for lookUpTableName in self._lookUpTables:
            self._integratedValues[lookUpTableName]=scipy.cumsum(self._interpolatedValues[lookUpTableName])
            
    def getIntegratedValuesDict(self):
        return self._integratedValues
    
    def getIntegratedValuesAtTime(self, time, variableName):
        timeIndex=(np.abs(self._timeVec-time)).argmin()
        return self._integratedValues[variableName][timeIndex],self._timeVec[timeIndex]


class BasicTurbine_Controllable():
    def __init__(self, lookUpTableGridValues, controllerLookUpTables, idlingLookUpTables, 
                 cutInWindSpeed,cutOutWindSpeed,
                 initWind, initOtherInput, 
                 lookUpTable_deltaT_hour=1/6, initTime=0, deltaT_hour=1/6, defaultController=0):
        
        self._gridValues=lookUpTableGridValues
        
        self._controllerLookUpTables = controllerLookUpTables
        
        self._lookUpTable_CurrentController=controllerLookUpTables[defaultController]
        
        self._idlingLookUpTables=idlingLookUpTables
        
        self._cutInWind=cutInWindSpeed
        
        self._cutOutWind=cutOutWindSpeed
        
        self._currentTime=initTime
        
        self._timeStepRatio=deltaT_hour/lookUpTable_deltaT_hour
        
        self._deltaT=deltaT_hour
        
        self._timeIndex=0
        
        # @reqnik: Why do you need a time vector?
        self._timeVec=[self._currentTime]
            
        self._currentIncrements = dict((varName,0) for varName in self._lookUpTable_CurrentController)
        
        self._incrementsTillCurrentTime = dict((varName,[]) for varName in self._lookUpTable_CurrentController)

        self._currentIntegrationValues=dict((varName,0) for varName in self._lookUpTable_CurrentController)
        
        self._integratedValues=dict((varName,[]) for varName in self._lookUpTable_CurrentController)
    
    
        
        self._setTurbineMode(initWind)
        
        self._calcCurrentIncrements(np.append(np.array(initWind),initOtherInput))
        
        self._sumIncrements()
        
        
    def _setControllerConfiguration(self,controllerConfig):
        self._lookUpTable_CurrentController=self._controllerLookUpTables[controllerConfig]
        
    def _setTurbineMode(self,windSpeed):
    # @reqnik: maybe replace this by a index value and store look up tables in a list
        if windSpeed < self._cutInWind:
            self._currentLookUpTables=self._idlingLookUpTables
        elif windSpeed > self._cutOutWind:
            self._currentLookUpTables=self._idlingLookUpTables
        else:
            self._currentLookUpTables=self._lookUpTable_CurrentController
            
    def _calcCurrentIncrements(self,windInputValues):
        for lookUpTableName in self._currentLookUpTables:
            
            lookUpValue=self._currentLookUpTables[lookUpTableName]
  
            interpolatedValue=functions.get_interpolation(self._gridValues, lookUpValue, windInputValues)
            
            interpolatedValue=max(0, interpolatedValue)
                  
            currentIncrement = interpolatedValue * self._timeStepRatio

            self._currentIncrements[lookUpTableName] = currentIncrement
            self._incrementsTillCurrentTime[lookUpTableName].append( currentIncrement)
            
            
    def _sumIncrements(self):
        for lookUpTableName in self._incrementsTillCurrentTime:
            self._currentIntegrationValues[lookUpTableName]+=self._currentIncrements[lookUpTableName]
            self._integratedValues[lookUpTableName].append(self._currentIntegrationValues[lookUpTableName])
            
            
    def update(self,windSpeed,otherWindInputs):
        self._timeIndex+=1
        self._currentTime=self._timeIndex * self._deltaT
        # @reqnik: could be calculated only if needed from the length of _incrementsTillCurrentTime
        self._timeVec.append(self._currentTime)
        
        self._setTurbineMode(windSpeed)
        self._calcCurrentIncrements(np.append(np.array(windSpeed),otherWindInputs))
        self._sumIncrements()
            
    def getIntegratedValueFromStartToCurrentDict(self):
        return self._integratedValues
    
    def getIncrementsFromStartToCurrentDict(self):
        return self._currentIntegrationValues
    
    def getCurrentIntegratedValuesDict(self):
        return self._integratedValues
    
    def getCurrentIncrementsDict(self):
        return self._currentIncrements
    
    def getTimeVec(self):
        return self._timeVec
    
    def getCurrentTime(self):
        return self._currentTime
