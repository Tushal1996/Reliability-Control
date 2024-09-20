#! /usr/bin/env python
# -*- coding:utf-8 -*-

'''
Created on 07.03.2019

@author: localadmin
'''
import os
import nt
import numpy as np
from ReliabilityControl.EvaluationMethods import BearinxWrapper
from scipy import io

if __name__ == '__main__': 
    windStrings=['04','06','08','10','12','14','16','18','20','22','24','26']
    turbStrings=['min2sig', 'minsig', 'sig', 'plsig', 'pl2sig'] 
    
    bearinxExecutablePath="C:\\IWESCalculator\\BearingCalculator\\MainBearingCalculator.exe"
    bearinxFolderPath="C:\\IWESCalculator\\BearingCalculator"
    configurationFilePath="C:\\IWESCalculator\\Configurations\\configLocalCalculation_longtermPresim.json"
    resultFolder='F:\\ReqNik\\Simulationen\\Bearinx\\out_longtermPresim'
#     resultFolder='\\\\iwes.fraunhofer.de\\Data\\Projekte\\112240-Propabilistik-SG\\30_Technische_Ausführung\\05_Lastrechnung\\ControllerLongtermSimulations\\BearinxResults\\out_longtermPresim'
    schaefflerDlcFolder='F:\\ReqNik\\Simulationen\\schaefflerCSV'
#     classificationFile='C:\\Users\\Reqnik\\Documents\\Schaeffler\\IPC\\schaefflerClassificationFile.txt'

    matOutFolder='F:\\ReqNik\\ControllerLongtermSimulations\\BearinxResults'

    
#     resultNums=['1','2','3','4','5','7','8','11']
    resultNums=['9','6']
    dirNameBase='F:\\ReqNik\\ControllerLongtermSimulations\\'

    for num in resultNums:
        outFile=matOutFolder+'\\results_'+num
        outDict={}
        
        
        dirNameOut=dirNameBase+'ResultsCSV\\results_'+num
        
        
        resultFolderConfig=resultFolder+'\\results_'+num
        bearinxWrapper = BearinxWrapper.BearinxWrapper(bearinxCalculatorFolderPath=bearinxFolderPath,bearinxExecutablePath=bearinxExecutablePath,
                                    configurationFilePath=configurationFilePath)
        mainBearingLhr_mat=np.zeros((len(windStrings),len(turbStrings)))
        gearBoxInputBearingLhr_mat=np.zeros((len(windStrings),len(turbStrings)))
        gearBoxInputBearingSID_mat=np.zeros((len(windStrings),len(turbStrings)))
        gearBoxBearingsTotal_mat=np.zeros((len(windStrings),len(turbStrings)))
        
        gearBoxAllSeperate_mats={}
        for windI,windString in enumerate(windStrings):
            for turbI,turbString in enumerate(turbStrings):
                print(str(num))
                
                keyString='windBin_'+windString+'_TI_'+turbString
                resultFolderWindTurb=resultFolderConfig+'\\'+keyString+'_allSeeds'
                print(keyString)

                bearinxWrapper.setResultFolder(resultFolderWindTurb)
                resultDirMainShaft=bearinxWrapper.getDynamicDamageCalculationsForMainshaft()
                          
                mainBearing_Lhr=resultDirMainShaft['F-623389.PRL_Lhr']
                gearBoxInputBearing_Lhr=resultDirMainShaft['SL1818/800-E-TB-BR_Lhr']
                gearBoxInputBearing_SID=resultDirMainShaft['SL1818/800-E-TB-BR_R_SID_max']
                  
                lh10ValsGearbox=bearinxWrapper.getLh10ValuesForGearbox()
                  
                gearBoxBearingsTotal=bearinxWrapper.getCombinedLh10ValuesForGearbox(lh10ValsGearbox)
      
                mainBearingLhr_mat[windI, turbI]=mainBearing_Lhr
                gearBoxInputBearingLhr_mat[windI, turbI]=gearBoxInputBearing_Lhr
                gearBoxInputBearingSID_mat[windI, turbI]=gearBoxInputBearing_SID 
                gearBoxBearingsTotal_mat[windI, turbI]=gearBoxBearingsTotal
                
#                 lh10ValsGearboxDir=bearinxWrapper.getDynamicDamageCalculationsForGearbox()
#                 for gearBoxBearing in lh10ValsGearboxDir:
#                     if gearBoxBearing not in gearBoxAllSeperate_mats:
#                         gearBoxAllSeperate_mats[gearBoxBearing]=np.zeros((len(windStrings),len(turbStrings)))
#                     gearBoxAllSeperate_mats[gearBoxBearing][windI,turbI]=lh10ValsGearboxDir[gearBoxBearing]
#         
#         gearBoxOutDir={}
#         numSID=0
#         numLh=0
#         for gearBoxBearing in gearBoxAllSeperate_mats:
#             if 'SID' in gearBoxBearing:
#                 gearBoxOutDir['GbSID'+str(numSID)]=gearBoxAllSeperate_mats[gearBoxBearing]
#                 numSID+=1
#             else:
#                 gearBoxOutDir['Gb'+str(numLh)]=gearBoxAllSeperate_mats[gearBoxBearing]
#                 numLh+=1

                
        
        outDict['config'+num+'_mainBearingLhr']=mainBearingLhr_mat
        outDict['config'+num+'_gearBoxInputBearingLhr']=gearBoxInputBearingLhr_mat
        outDict['config'+num+'_gearBoxInputBearingSID']=gearBoxInputBearingSID_mat
        outDict['config'+num+'_gearBoxBearingsTotal']=gearBoxBearingsTotal_mat
   
        io.savemat(outFile, outDict)
#         io.savemat(outFile, gearBoxOutDir)

