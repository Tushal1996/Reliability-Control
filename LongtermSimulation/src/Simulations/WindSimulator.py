
import numpy as np
import pandas as pd
from InterpolationFunction import get_interpolation
import ReliabilityControllerSimulator as Controller

class WindSimulation:

    def __init__(self, objectiveValuesLookUp, LoadObj, EnergyObj, initWind, initBval
                 , initTime = 0):
        self._objectiveLookupValues = objectiveValuesLookUp
        self._integrator = 0
        self._timeIndex = 0
        self._currentTime = initTime
        self._currentIncrement = 0
        self._energyObj = EnergyObj
        self._loadObj = LoadObj
        self._timeVec = []
        self._desiredHealthIndexVec = []
        self._currentHealthIndexVec = []
        self._configurationVec = []
        self.D_nom = 0.95
        self.HI_0 = 1.0
        self.HI_des_end = 0.0
        self.t_spec = 2 * 525600

    def update(self, currentConfiguration, WindSpeed, Bval):

        self._currentTime = self._timeIndex
        self._timeVec.append(self._currentTime)
        self._timeIndex += 1

        self._configurationVec.append(currentConfiguration[0])
        self._getObjectiveValuesFromWindSimulationLookupTable(currentConfiguration, WindSpeed, Bval)
        return self._currentIncrement

    def _getObjectiveValuesFromWindSimulationLookupTable(self, currentConfiguration, WindSpeed, Bval):

        interpolatedLoad = get_interpolation(pd.DataFrame((self._objectiveLookupValues[currentConfiguration[0] - 1][self._loadObj])).values, (WindSpeed, Bval))
        interpolatedEnergy = get_interpolation(pd.DataFrame((self._objectiveLookupValues[currentConfiguration[0] - 1][self._energyObj])).values, (WindSpeed, Bval))
        self._currentIncrement += interpolatedLoad

    def _getDeltaHealthIndex(self):
        desiredHealthIndex = self.HI_0 - (((self.HI_0 - self.HI_des_end) / self.t_spec) * self._timeIndex)
        self._desiredHealthIndexVec.append(desiredHealthIndex)
        currentHealthIndex = 1 - (self._currentIncrement / self.D_nom)
        self._currentHealthIndexVec.append(currentHealthIndex)
        deltaHI = desiredHealthIndex - currentHealthIndex
        return deltaHI

    def _getTimeVec(self):
        return self._timeVec

    def _getDesiredHealthIndexVec(self):
        return self._desiredHealthIndexVec

    def _getCurrentHealthIndexVec(self):
        return self._currentHealthIndexVec

    def _getCurrentConfigurationVec(self):
        return self._configurationVec

    # =================================================================================================================
    # =================================================================================================================

    def _getCurrentHealthIndex(self):
        currentHealthIndex = 1 - (self._currentIncrement/self.D_nom)
        return currentHealthIndex

    def _getDesiredHealthIndex(self):
        desiredHealthIndex = self.HI_0 - (((self.HI_0 - self.HI_des_end) / self.t_spec) * self._timeIndex)
        return desiredHealthIndex

    def _getTimeIndex(self):
        return self._timeIndex