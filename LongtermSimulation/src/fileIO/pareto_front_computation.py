import pandas as pd
import numpy as np
import math
from scipy.io import savemat
import argparse
import sys
import matplotlib.pyplot as plt
import scipy.io
from scipy.io import loadmat


class AlphaParameterization:

    def __init__(self, pareto_load, pareto_energy):

        self._maxEnergy = max(pareto_energy)
        self._minEnergy = min(pareto_energy)
        self._maxLoad = max(pareto_load)
        self._minLoad = min(pareto_load)
        self._paretoLoad = pareto_load
        self._paretoEnergy = pareto_energy

    def _getParetoFront(self):

        slope = -((self._minEnergy - self._maxEnergy) / (self._minLoad - self._maxLoad))    # slope of a linear function
        objective_values = list(zip(self._paretoLoad, self._paretoEnergy))    # Objective pairs

        alpha_current = []
        for x, y in objective_values:
             # Intersection points (f1_s, f2_s)
             f1_s = (self._maxEnergy - y + ((x * (self._minLoad - self._maxLoad)) / (self._minEnergy - self._maxEnergy)) + (
                (self._minLoad * (self._minEnergy - self._maxEnergy)) / (self._minLoad - self._maxLoad))) \
               / (((self._minLoad - self._maxLoad) / (self._minEnergy - self._maxEnergy)) + ((self._minEnergy - self._maxEnergy) / (self._minLoad - self._maxLoad)))
             f2_s = self._maxEnergy + slope * (f1_s - self._minLoad)

             # distances
             D_p = math.sqrt(((self._maxLoad - self._minLoad) ** 2) + ((self._minEnergy - self._maxEnergy) ** 2))
             D_a = math.sqrt(((self._maxLoad - f1_s) ** 2) + ((self._minEnergy - f2_s) ** 2))

             # The current value of the alpha-parameterization
             alpha_cur = 1 - ((2 * D_a) / D_p)
             alpha_current.append(alpha_cur)

        return alpha_current

    def _getPlotForAlphaParameterization(self):

        slope = -((self._minEnergy - self._maxEnergy) / (self._minLoad - self._maxLoad))  # slope of a linear function
        paretoEnergy = []
        paretoLoad = np.array(self._paretoLoad)
        for f1 in paretoLoad:     # Define Linear Function
            f2_initial = self._maxEnergy + slope * (f1 - self._minLoad)
            paretoEnergy.append(f2_initial)
        plt.figure()
        plt.title('Alpha-Parameterization')
        plt.plot(ParetoLoad, ParetoEnergy, 'o--', label='Pareto Optimal Configuration')
        plt.plot(paretoLoad, paretoEnergy, 'r-', label='Alpha Parameterization')
        plt.xlabel('ParetoLoad')
        plt.ylabel('ParetoEnergy')
        plt.legend(loc='upper right')
        plt.grid()
        plt.show()



if __name__ == '__main__':

    ParetoOptimal = scipy.io.loadmat('ParetoOptimalArray_Flap.mat')     # Load the pareto optimal .mat file
    del ParetoOptimal['__header__']
    del ParetoOptimal['__version__']
    del ParetoOptimal['__globals__']

    ParetoOptimalList = list(ParetoOptimal.values())
    EnergyObj = []        # Empty list to append the energy optimal pareto point
    LoadObjective = []    # Empty list to append the load optimal pareto point
    for x in ParetoOptimalList:
        for a in x:
            EnergyObj.append(a[0])
            LoadObjective.append(a[1])

    EnergyObjective = [-item for item in EnergyObj]   # Minimize the Energy Objective
    ParetoLoad, ParetoEnergy = zip(*sorted(zip(LoadObjective, EnergyObjective))) # Sort the ParetoLoad and ParetoObjective

    ParetoOptimalValues = AlphaParameterization(ParetoLoad, ParetoEnergy)

    ParetoOptimalValues._getPlotForAlphaParameterization()   # call the _getPlotForAlphaParameterization function to plot the pareto optimal configurations
    alphaValue = ParetoOptimalValues._getParetoFront()   # call the _getParetoFront function to get the alpha values
    print(alphaValue)

    # alphaValue = pd.DataFrame(pareto_front(ParetoLoad, ParetoEnergy), columns=['alpha'])  # Alpha Values in Pandas Dataframe
    # scipy.io.savemat('AlphaValue_Blade1_Flapwise_.mat', {'alpha': alphaValue})   # Save the alpha values for PI-Controller gain scheduling
