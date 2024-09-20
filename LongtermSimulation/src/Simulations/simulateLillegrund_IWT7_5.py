#! /usr/bin/env python
# -*- coding:utf-8 -*-

'''
Created on 18.09.2019

@author: reqnik
'''
import sys
sys.path.append('\\\\iwes.fraunhofer.de\\Data\\OE\\OE200_STUD\\Tushal_Patel\\LongtermSimulation\\src')
sys.path.append(r'C:\Users\pattus\Desktop\FRAUNHOFER_IWES\LongtermSim_Niklas\LongtermSimulation\src')
import pandas as pd
from pathlib import Path
import numpy as np
from Simulations import functions
import scipy.io
from Simulations import Simulator
from fileIO import loadDataForLongtermSim
from matplotlib import pyplot as plt
import copy
import matplotlib as mpl
mpl.rc('figure', max_open_warning = 0)


if __name__ == '__main__':
    scadaData_Lillgrund=pd.read_csv(Path(r'C:\Users\pattus\Desktop\FRAUNHOFER_IWES\LongtermSim_Niklas\Input_Lillgrund\SCADA_Lillgrund.csv'),',')#
    B_func_parameters=scipy.io.loadmat(Path(r'C:\Users\pattus\Desktop\FRAUNHOFER_IWES\LongtermSim_Niklas\Input_Lillgrund\B_func_parameters.mat'))['B_func_parameters'][0]
    lookUpTables=loadDataForLongtermSim.loadMatFileWithLookUpTables(Path(r'C:\Users\pattus\Desktop\FRAUNHOFER_IWES\LongtermSim_Niklas\Input_Lillgrund\lookUpTables_Lillgrund.mat') )

    scada_Lillgrund_NaNFilter=scadaData_Lillgrund.dropna(subset=['WdSpdAv','WdSpdMax','WdSpdMin','WdSpdSdv'])
    windColName='WdSpdAv'
    stdColName='WdSpdSdv'
    
    dateTime=np.array(scada_Lillgrund_NaNFilter.loc[:, 't'])

    windSpeedVec_scada=np.array(scada_Lillgrund_NaNFilter.loc[:, windColName])
    stdDev=np.array(scada_Lillgrund_NaNFilter.loc[:, stdColName])
    
    windNonZeroIndex=np.where(windSpeedVec_scada!=0)
    
    windSpeedVec_scada=windSpeedVec_scada[windNonZeroIndex]   
    stdDev=stdDev[windNonZeroIndex]    
    dateTime=dateTime[windNonZeroIndex]    


    stdDevNonZeroIndex=np.where(stdDev!=0)
    
    windSpeedVec_scada=windSpeedVec_scada[stdDevNonZeroIndex]   
    stdDev=stdDev[stdDevNonZeroIndex]
    dateTime=dateTime[stdDevNonZeroIndex]    
  
    
    TI=stdDev/windSpeedVec_scada
    
    
    B_trans=functions.B_transformation(B_func_parameters)
    B_vals_scada=B_trans.calcB(windSpeedVec_scada,TI)

    
    windBinCenterValues=list(range(4,34,2))
    B_values=[-2,-1,0,1,2]
    
    

    idlingLookUpTables = copy.deepcopy(lookUpTables)
    idlingLookUpTables['Energy']=np.zeros((len(windBinCenterValues),len(B_values)))
    
    turbine_controllable=Simulator.BasicTurbine_Controllable([windBinCenterValues,B_values],[lookUpTables],idlingLookUpTables,
                                                             cutInWindSpeed=3,cutOutWindSpeed=26,
                                                             initWind=windSpeedVec_scada[0],initOtherInput=np.array([B_vals_scada[0]]))
    
    
    for windI,windSpeed in enumerate(windSpeedVec_scada[1:]):
        otherInput=np.array(B_vals_scada[windI])
        turbine_controllable.update(windSpeed,otherInput)
        print('Time: ' + dateTime[1:][windI])
        print('windspeed: ' +str(windSpeed))
        
    resultDict_controllable=turbine_controllable.getIntegratedValueFromStartToCurrentDict()
    timeVec_controllable=turbine_controllable.getTimeVec()
#     cProfile.run('simulateTurbine(turbine_controllable,inputData)')

    for varName in resultDict_controllable:
        plt.figure()
        plt.plot(timeVec_controllable,resultDict_controllable[varName],label='controllable turbine + no extrapolation')
        plt.ylabel(varName)
        plt.xlabel('time in h')
        plt.legend(loc="best")
 
    plt.show()
