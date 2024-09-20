import os
from scipy.io import loadmat
import pandas as pd
import numpy as np
from pandas import DataFrame
import sys


def WindSimulationLookUpTable(PreSimulationFolderPath):
    # cwd = os.getcwd()
    os.chdir(PreSimulationFolderPath)
    entries = os.listdir(PreSimulationFolderPath)
    controller_configurations = []
    for file in entries:
        controller_configurations.append(loadmat(file))

    return controller_configurations



