
import numpy as np
import pandas as pd
from InterpolationFunction import get_interpolation


class ReliabilityController:

    def __init__(self, objectiveValuesLookUp, gainSchedulingLookUp, LoadObj, EnergyObj, initConfiguration, initWind, initBval
                 , deltaT = 1, alphaLowerBound = -1, alphaUpperBound = 1, initTime = 0):

        self._objectiveLookupValues = objectiveValuesLookUp
        self._gainSchedulingLookupValues = gainSchedulingLookUp
        self._currentConfiguration = initConfiguration
        self._integrator = 0
        self.alphaLowerBound = alphaLowerBound
        self.alphaUpperBound = alphaUpperBound
        self._deltaT = deltaT

        self._timeIndex = 0
        self._currentTime = initTime
        self._currentIncrement = 0
        self.D_nom = 0.95
        self.HI_0 = 1.0
        self.HI_des_end = 0.0
        self.t_spec = 2 * 525600
        self._timeVec = []
        self._desiredHealthIndexVec = []
        self._currentHealthIndexVec = []
        self._configurationVec = []
        self._energyObj = EnergyObj
        self._loadObj = LoadObj

    def update(self, deltaHI, WindSpeed, Bval):

        self._currentTime = self._timeIndex
        self._timeVec.append(self._currentTime)
        self._timeIndex += 1

        self._getGainFromScheduling(WindSpeed, Bval)
        self.integrate(deltaHI)

        alpha = self._kP*deltaHI + self._integrator
        alpha = max(alpha, self.alphaLowerBound)
        alpha = min(alpha, self.alphaUpperBound)

        self._searchNearestConfiguration(alpha)
        self._getObjectiveValuesFromWindSimulationLookupTable(WindSpeed, Bval)
        return self._currentIncrement

    def integrate(self, deltaHI):

        self._integrator += (self._kI * deltaHI * self._deltaT)
        self._integrator = max(self._integrator, self.alphaLowerBound)
        self._integrator = min(self._integrator, self.alphaUpperBound)

    def _getGainFromScheduling(self, WindSpeed, Bval):

        self._kP = get_interpolation(pd.DataFrame((self._gainSchedulingLookupValues['kp'][self._currentConfiguration[0] -1])).values, (WindSpeed, Bval))
        self._kI = get_interpolation(pd.DataFrame((self._gainSchedulingLookupValues['ki'][self._currentConfiguration[0] -1])).values, (WindSpeed, Bval))

    def _searchNearestConfiguration(self, alphaDesired):

        NearestConfiguration = self._gainSchedulingLookupValues.loc[(self._gainSchedulingLookupValues['alpha'] - alphaDesired).abs().argsort()[:2]]
        self._currentConfiguration = NearestConfiguration.iloc[0, 0:1].values
        self._configurationVec.append(self._currentConfiguration[0])

    def _getObjectiveValuesFromWindSimulationLookupTable(self, WindSpeed, Bval):

        interpolatedLoad = get_interpolation(pd.DataFrame((self._objectiveLookupValues[self._currentConfiguration[0] - 1][self._loadObj])).values, (WindSpeed, Bval))
        interpolatedEnergy = get_interpolation(pd.DataFrame((self._objectiveLookupValues[self._currentConfiguration[0] - 1][self._energyObj])).values, (WindSpeed, Bval))
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

# =====================================================================================================================
# =====================================================================================================================
# =====================================================================================================================


    def _getCurrentHealthIndex(self):
        currentHealthIndex = 1 - (self._currentIncrement/self.D_nom)
        return currentHealthIndex

    def _getDesiredHealthIndex(self):
        desiredHealthIndex = self.HI_0 - (((self.HI_0 - self.HI_des_end) / self.t_spec) * self._timeIndex)
        return desiredHealthIndex

    def _getTimeIndex(self):
        return self._timeIndex







