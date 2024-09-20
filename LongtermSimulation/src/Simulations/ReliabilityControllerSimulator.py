
import numpy as np
import pandas as pd
from InterpolationFunction import get_interpolation

class ReliabilityController:

    def __init__(self, gainSchedulingLookUp, initConfiguration, initWind, initBval, setWeightProp, setWeighInt, setWeightDer
                 , deltaT = 1, alphaLowerBound = -1, alphaUpperBound = 1, initTime = 0):

        self._gainSchedulingLookupValues = gainSchedulingLookUp
        self._currentConfiguration = initConfiguration
        self._integrator = 0
        self._derivator = 0
        self._timeIndex = 0
        self._currentTime = initTime
        self.alphaLowerBound = alphaLowerBound
        self.alphaUpperBound = alphaUpperBound
        self._deltaT = deltaT
        self._setWeightProp = setWeightProp
        self._setWeightInt = setWeighInt
        self._setWeightDer = setWeightDer

    def update(self, deltaHI, WindSpeed, Bval):
        self._currentTime = self._timeIndex
        self._timeIndex += 1

        self._getGainFromScheduling(WindSpeed, Bval)
        self.integrate(deltaHI)

        alpha = self._kP * self._setWeightProp * deltaHI + self._integrator + (deltaHI - self._derivator) * self._kD * self._setWeightDer
        self._derivator = deltaHI
        alpha = max(alpha, self.alphaLowerBound)
        alpha = min(alpha, self.alphaUpperBound)

        self._searchNearestConfiguration(alpha)
        return self._currentConfiguration

    def integrate(self, deltaHI):

        self._integrator += (self._kI *self._setWeightInt* deltaHI * self._deltaT)
        self._integrator = max(self._integrator, self.alphaLowerBound)
        self._integrator = min(self._integrator, self.alphaUpperBound)

    def _getGainFromScheduling(self, WindSpeed, Bval):

        self._kP = get_interpolation(pd.DataFrame((self._gainSchedulingLookupValues['kp'][self._currentConfiguration[0] -1])).values, (WindSpeed, Bval))
        self._kI = get_interpolation(pd.DataFrame((self._gainSchedulingLookupValues['ki'][self._currentConfiguration[0] -1])).values, (WindSpeed, Bval))
        self._kD = get_interpolation(pd.DataFrame((self._gainSchedulingLookupValues['kd'][self._currentConfiguration[0] - 1])).values, (WindSpeed, Bval))

    def _searchNearestConfiguration(self, alphaDesired):

        NearestConfiguration = self._gainSchedulingLookupValues.loc[(self._gainSchedulingLookupValues['alpha'] - alphaDesired).abs().argsort()[:2]]
        self._currentConfiguration = NearestConfiguration.iloc[0, 0:1].values


# =====================================================================================================================
# =====================================================================================================================
# =====================================================================================================================









