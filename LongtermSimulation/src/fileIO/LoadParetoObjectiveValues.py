import pandas as pd
import numpy as np
import os
import sys
from pareto_front_computation import pareto_front
import matplotlib.pyplot as plt
from scipy.io import savemat
import scipy.io
from scipy.io import loadmat
import tables


def LoadOptimalParetoValue(MatFile):
    ParetoOptimal = scipy.io.loadmat(MatFile)
    del ParetoOptimal['__header__']
    del ParetoOptimal['__version__']
    del ParetoOptimal['__globals__']

    ParetoOptimalList = list(ParetoOptimal.values())
    EnergyObj = []
    LoadObjective = []
    for x in ParetoOptimalList:
        for a in x:
            EnergyObj.append(a[0])
            LoadObjective.append(a[1])
    EnergyObjective = [-item for item in EnergyObj]
    ParetoLoad, ParetoEnergy = zip(*sorted(zip(LoadObjective, EnergyObjective)))
    # alphaValue = pd.DataFrame(pareto_front(ParetoLoad, ParetoEnergy), columns=['alpha'])
    alphaValue = pareto_front(ParetoLoad, ParetoEnergy)
    # scipy.io.savemat('AlphaValue_Blade1_Flapwise_.mat', {'alpha': alphaValue})

    return alphaValue


def find_nearest_alpha(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]


def AlphaSearch(ParetoOptimalMatFile, ControllerOutput):
    ParetoFront = LoadOptimalParetoValue(ParetoOptimalMatFile)
    AlphaCurrent = find_nearest_alpha(ParetoFront, ControllerOutput)
    print(AlphaCurrent)

    return AlphaCurrent



if __name__ == '__main__':

    # AlphaSearch('ParetoOptimalArray_Edge.mat', 0.3)

    LoadOptimalParetoValue('ParetoOptimalArray_Flap.mat')
    # index = pareto_configuration.loc[(pareto_configuration['alpha'] - alpha_current).abs().argsort()[:2]]



# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


# loadParetoObjectiveValue(r'C:\Users\pattus\Desktop\FRAUNHOFER_IWES\LongtermSim_Niklas\Input_Lillgrund\LifetimeDels_IWT7_5')

# def loadParetoObjectiveValue (path):
#     # print(os.getcwd())
#     # print(os.listdir(os.getcwd()))
#     os.chdir(path)
#     entries = os.listdir(path)
#     controller_configurations = []
#     for file in entries:
#         controller_configurations.append(pd.read_csv(file))
#
#     paretoValue = pd.concat(controller_configurations, sort=False)
#     pareto_load = list(paretoValue['HubFx'])
#     pareto_energy = [-item for item in list(paretoValue[' Energy'])]     # Minimization of energy objective
#
#     ParetoLoad, ParetoEnergy = zip(*sorted(zip(pareto_load, pareto_energy)))
#     alphaValue = pareto_front(ParetoLoad, ParetoEnergy)
#     # scipy.io.savemat('AlphaValue_HubFx_Energy.mat', {'alpha': alphaValue})
#
#     return alphaValue