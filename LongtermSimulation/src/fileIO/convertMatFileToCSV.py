#! /usr/bin/env python
# -*- coding:utf-8 -*-


'''
Created on 06.03.2019

@author: localadmin
'''

from scipy import io
import nt
import os
import numpy as np
from ReliabilityControl.EvaluationMethods import BearinxWrapper

def renameFiles(dirname,filenames):
    for filename in filenames:
        nameSplit = filename.split('_')
        windAndTI = nameSplit[5]
        wind = windAndTI.split('T')[0]
        
        if len(wind)==1:
            wind= "0" + wind
        filename_new =filename.replace(nameSplit[5],wind+'_TI')
        old_file = os.path.join(dirname, filename)
        new_file = os.path.join(dirname, filename_new)
        os.rename(old_file, new_file)
        

    
if __name__ == '__main__': 
    
    dirNameBase='F:\\ReqNik\\ControllerLongtermSimulations\\'
    resultNums=['10','12','13']
    schaefflerHeader=['Time','vHub','rotorSpeed','mainBearing_F_stat_x','mainBearing_F_stat_y','mainBearing_F_stat_z','mainBearing_T_stat_x','mainBearing_T_stat_y','mainBearing_T_stat_z']
    outputStartTime=20
    schaefflerCols=range(1,9)
    for num in resultNums:
        dirNameMat=dirNameBase+'ResultsMat\\results_'+num
    
        listFiles=nt.listdir(dirNameMat)
#         renameFiles(dirNameMat, listFiles)

        
        dirNameOut=dirNameBase+'ResultsCSV\\results_'+num
 
        if not os.path.exists(dirNameOut):
            os.makedirs(dirNameOut)
        for file in listFiles:
            matData=io.loadmat(dirNameMat+'\\'+file)
            res=matData['simout']
            timeVec=res[0,0][0]
            data=np.append(timeVec,res[0,0][1][0][0][0],axis=1).T
            timeVec=data[0]
            data[2]=data[2]*30/np.pi
              
            outputStartIndex=np.where(abs(timeVec-outputStartTime)<1e-6)[0][0]
            timeVec=timeVec[outputStartIndex:]-outputStartTime
            schaefflerInput=[['[s]'],['[m/s]'],['[1/min]'],['[N]'],['[N]'],['[N]'],['[Nm]'],['[Nm]'],['[Nm]']]
            fileName=file.split('.')[0]
            keyFileName=fileName+'.csv'
              
            BearinxWrapper.writeCsvFilesForBearinx(data, schaefflerInput,schaefflerHeader, dirNameOut,schaefflerCols,
                                                    timeVec, keyFileName, outputStartIndex)
