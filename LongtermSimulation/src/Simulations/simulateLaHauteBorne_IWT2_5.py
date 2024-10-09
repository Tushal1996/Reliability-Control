#! /usr/bin/env python
# -*- coding:utf-8 -*-

'''
Created on 02.09.2019


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
import cProfile#
import copy
    
def simulateTurbine(turbine_controllable,windSpeedVec_scada,B_vals_scada): 
    for windI,windSpeed in enumerate(windSpeedVec_scada[1:]):
        otherInput=np.array(B_vals_scada[windI])
        turbine_controllable.update(windSpeed,otherInput)
    return turbine_controllable
if __name__ == '__main__':
# =============================================================================
#     Load data
# =============================================================================
    laHauteBorne_csv=pd.read_csv(Path(r'C:\Users\pattus\Desktop\FRAUNHOFER_IWES\LongtermSim_Niklas\Input_LaHauteBorne\SCADA_LaHaute.csv'),delimiter=',')
    wind_B_values=scipy.io.loadmat(Path(r'C:\Users\pattus\Desktop\FRAUNHOFER_IWES\LongtermSim_Niklas\Input_LaHauteBorne\wind_B_Bfunc_values.mat'))
    lookUpTables=loadDataForLongtermSim.loadMatFileWithLookUpTables(Path(r'C:\Users\pattus\Desktop\FRAUNHOFER_IWES\LongtermSim_Niklas\Input_LaHauteBorne\LookUpTablesLaHauteBorne.mat') )
    
# =============================================================================
#     Adaption of Lookup-tables for results of Bearinx (Schäffler-Tool)
# =============================================================================
    lookUpTables['config1_gearBoxBearingsTotal']=1/(6*lookUpTables['config1_gearBoxBearingsTotal'])
    lookUpTables['config1_gearBoxInputBearingLhr']=1/(6*lookUpTables['config1_gearBoxInputBearingLhr'])
    lookUpTables['config1_mainBearingLhr']=1/(6*lookUpTables['config1_mainBearingLhr'])
    del lookUpTables['config1_gearBoxInputBearingSID']
    
    windColName='Ws_avg'
    stdColName='Ws_std'
    pd.set_option('use_inf_as_na', True)

# =============================================================================
# Filter of NaN - values
# =============================================================================
    scada_LaHaute_NaNFilter=laHauteBorne_csv.dropna(subset=['Ws_avg','Ws1_avg','Ws2_avg','S_avg','Ws_std','Ba_avg','Rs_avg'])

    windSpeedVec_scada=laHauteBorne_csv.loc[:, windColName]
    stdDev=laHauteBorne_csv.loc[:, stdColName]
    
    dateTime=np.array(scada_LaHaute_NaNFilter.loc[:, 'Date_time'])


    windSpeedVec_scada=np.array(scada_LaHaute_NaNFilter.loc[:, windColName])
    stdDev=np.array(scada_LaHaute_NaNFilter.loc[:, stdColName])
    
# =============================================================================
# Filter of zeros-values (could be replaced by your filter function)
# =============================================================================
    windNonZeroIndex=np.where(windSpeedVec_scada!=0)
    
    windSpeedVec_scada=windSpeedVec_scada[windNonZeroIndex]   
    stdDev=stdDev[windNonZeroIndex]    
    dateTime=dateTime[windNonZeroIndex]    


    stdDevNonZeroIndex=np.where(stdDev!=0)
    
    windSpeedVec_scada=windSpeedVec_scada[stdDevNonZeroIndex]   
    stdDev=stdDev[stdDevNonZeroIndex]
    dateTime=dateTime[stdDevNonZeroIndex]    
  
    
    
    B_trans=functions.B_transformation(wind_B_values['Bfunc_parameters'][0])
    
    B_vals_scada=B_trans.calcBFromSTD(np.array(windSpeedVec_scada), np.array(stdDev))

 
#===============================================================================
# Simulation by interpolating each value at a time with call of update (for possibility of control) -> no Extrapolation
#===============================================================================
    
    idlingLookUpTables = copy.deepcopy(lookUpTables)
    idlingLookUpTables['Energy_prod_600s']=np.zeros((len(wind_B_values['windBinCenterValues'][0]),len(wind_B_values['B_values'][0])))
    
    turbine_controllable=Simulator.BasicTurbine_Controllable([wind_B_values['windBinCenterValues'][0],wind_B_values['B_values'][0]],[lookUpTables],idlingLookUpTables,
                                                             cutInWindSpeed=3,cutOutWindSpeed=23,
                                                             initWind=windSpeedVec_scada[0],initOtherInput=np.array([B_vals_scada[0]]))
    
    
    for windI,windSpeed in enumerate(windSpeedVec_scada[1:]):
        otherInput=np.array(B_vals_scada[1:][windI])
        turbine_controllable.update(windSpeed,otherInput)
        print('Time: ' + dateTime[1:][windI])
        print('windspeed: ' +str(windSpeed))
        
    resultDict_controllable=turbine_controllable.getIntegratedValueFromStartToCurrentDict()
    timeVec_controllable=turbine_controllable.getTimeVec()
# =============================================================================
# plots all Simulated variables
# =============================================================================
    for varName in resultDict_controllable:
        plt.figure()
        plt.plot(timeVec_controllable,resultDict_controllable[varName])
        plt.ylabel(varName)
        plt.xlabel('time in h')
        plt.legend(loc="best")
# =============================================================================
#  plots selected simulate variable
# =============================================================================
    plt.figure()
    plt.plot(timeVec_controllable,resultDict_controllable['Energy_prod_600s'])
    plt.ylabel('Energy')
    plt.xlabel('time in h')
    plt.show()
    
    
