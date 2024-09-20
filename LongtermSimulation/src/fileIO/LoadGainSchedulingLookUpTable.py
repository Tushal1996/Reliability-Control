from scipy.io import loadmat
import pandas as pd
import numpy as np
import os
from InterpolationFunction import get_interpolation
from pandas import DataFrame
import sys

def GainSchedulingLookUpTable (GainFilename):

    LookUpTable = loadmat(GainFilename)
    del LookUpTable['__header__']
    del LookUpTable['__version__']
    del LookUpTable['__globals__']

    GainSchedulingLookup = {}
    GainSchedulingLookup.update(LookUpTable)
    GainSchedulingLookUpTable = pd.DataFrame((GainSchedulingLookup['Gain']), columns=['kp', 'ki', 'kd', 'alpha'])
    GainLookUp = GainSchedulingLookUpTable[['kp', 'ki', 'kd']]
    alphaValue = pd.DataFrame([float(x) for [x] in GainSchedulingLookUpTable['alpha']], columns=['alpha'])
    alphaIndex = pd.DataFrame(list(range(1, len(alphaValue) + 1)), columns=['index'])
    GainsLookUpTable = pd.concat([alphaIndex, alphaValue, GainLookUp], axis=1)

    return GainsLookUpTable


# =====================================================================================================================
# =====================================================================================================================
# =====================================================================================================================
# def AlphaSearch(PIControllerOutput):
#
#     Gain = GainSchedulingLookUpTable()
#     NearestAlpha = Gain.loc[(Gain['alpha'] - PIControllerOutput).abs().argsort()[:2]]
#     CurrentAlpha = NearestAlpha.iloc[0, 0:1]
#     CurrentAlphaGains = NearestAlpha.iloc[0, 1:3]
#
#     return CurrentAlpha, CurrentAlphaGains
#
# def GainScheduling(Wint, Binit):
#
#     CurrentAlpha = AlphaSearch()
#     GainLookup = CurrentAlpha.iloc[0, 1:3]
#     kp = get_interpolation(pd.DataFrame((GainLookup['kp'])).values, (initWind, initB))
#     ki = get_interpolation(pd.DataFrame((GainLookup['ki'])).values, (initWind, initB))
#     print(kp)
#     print(ki)
#     return GainLookUpTable


# def GainScheduling(GainFilename, index, initWind, initB):
#
#     Gains = GainSchedulingLookUpTable(GainFilename)
#     kp = get_interpolation(pd.DataFrame((Gains['kp'][index])).values, (initWind, initB))
#     ki = get_interpolation(pd.DataFrame((Gains['ki'][index])).values, (initWind, initB))
#
#     return kp, ki

