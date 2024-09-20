

import sys
import os

sys.path.append(r'C:\Users\tusha\OneDrive\Desktop\LongtermSim_Tushal\LongtermSimulation\src')
sys.path.append(r'C:\Users\tusha\OneDrive\Desktop\LongtermSim_Tushal\LongtermSimulation\src\Simulations')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from Simulations import functions
from InterpolationFunction import get_interpolation
from fileIO import LoadWindSimulationLookUpTable
from fileIO import LoadGainSchedulingLookUpTable
from Simulations import Simulator
from Simulations import ReliabilityControlSimulator
import scipy.io
import matplotlib.animation as animation
from pyqtgraph.Qt import QtGui, QtCore
from collections import deque
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
from PyQt5 import QtWidgets, uic, QtCore
from Simulations import ReliabilityControllerSimulator
from Simulations import WindSimulator
import time
from matplotlib.animation import FuncAnimation


if __name__ == '__main__':

    start = time.time()
    scadaData_Lillgrund = pd.read_csv(r'C:\Users\tusha\OneDrive\Desktop\LongtermSim_Tushal\Input_Lillgrund\SCADA_Lillgrund.csv', ',')  #
    B_func_parameters = scipy.io.loadmat(r'C:\Users\tusha\OneDrive\Desktop\LongtermSim_Tushal\Input_Lillgrund\B_func_parameters.mat')['B_func_parameters'][0]
    GainSchedulinLookUpTable = LoadGainSchedulingLookUpTable.GainSchedulingLookUpTable('Blade_Mx_root_gain_scheduling.mat')
    WindSimulationLookUpTables = LoadWindSimulationLookUpTable.WindSimulationLookUpTable(r'C:\Users\tusha\OneDrive\Desktop\LongtermSim_Tushal\LongtermSimulation\src\Simulations\ParetoOptimalLookUpTable')

    scada_Lillgrund_NaNFilter = scadaData_Lillgrund.dropna(subset=['WdSpdAv', 'WdSpdMax', 'WdSpdMin', 'WdSpdSdv'])
    windColName = 'WdSpdAv'
    stdColName = 'WdSpdSdv'

    dateTime = np.array(scada_Lillgrund_NaNFilter.loc[:, 't'])

    windSpeedVec_scada = np.array(scada_Lillgrund_NaNFilter.loc[:, windColName])
    stdDev = np.array(scada_Lillgrund_NaNFilter.loc[:, stdColName])

    windNonZeroIndex = np.where(windSpeedVec_scada != 0)

    windSpeedVec_scada = windSpeedVec_scada[windNonZeroIndex]
    stdDev = stdDev[windNonZeroIndex]
    dateTime = dateTime[windNonZeroIndex]

    stdDevNonZeroIndex = np.where(stdDev != 0)

    windSpeedVec_scada = windSpeedVec_scada[stdDevNonZeroIndex]
    stdDev = stdDev[stdDevNonZeroIndex]
    dateTime = dateTime[stdDevNonZeroIndex]

    TI = stdDev / windSpeedVec_scada

    B_trans = functions.B_transformation(B_func_parameters)
    B_vals_scada = B_trans.calcB(windSpeedVec_scada, TI)

    windBinCenterValues = list(range(4, 34, 2))
    B_values = [-2, -1, 0, 1, 2]

    LoadObj = 'Blade_Mx_root_mean'
    EnergyObj = 'Energy'

    reliabilityControlTurbine = ReliabilityControllerSimulator.ReliabilityController(GainSchedulinLookUpTable,
                                                                                     initConfiguration=[1],
                                                                                     initWind=windSpeedVec_scada[0],
                                                                                     initBval=np.array(
                                                                                         [B_vals_scada[0]]),
                                                                                     setWeightProp=1.0,
                                                                                     setWeighInt=1.0, setWeightDer=1.0)

    windSimulationLillegrund = WindSimulator.WindSimulation(WindSimulationLookUpTables, LoadObj, EnergyObj,
                                                            initWind=windSpeedVec_scada[0],
                                                            initBval=np.array([B_vals_scada[0]]))

    # ================================================================================================================
    # =================================================================================================================
    # plt.ion()
    # fig = plt.figure()
    # plt.grid()
    # plt.show(block=False)
    #
    # # HI_current = list()
    # # HI_desired = list()
    # # timeVec = list()
    # # configurationVec = list()
    #
    # for windI, WindSpeed in enumerate(windSpeedVec_scada[1:]):
    #     otherInput = np.array(B_vals_scada[windI])
    #
    #     deltaHI = windSimulationLillegrund._getDeltaHealthIndex()      # return the difference between HIcur and HIdes
    #     currentConfiguration = reliabilityControlTurbine.update(deltaHI, WindSpeed, otherInput)    # return the current configuration
    #     currentIncrement = windSimulationLillegrund.update(currentConfiguration, WindSpeed, otherInput)  # return the current increment
    #
    #     print('Time: ' + dateTime[1:][windI])
    #     print('windspeed: ' + str(WindSpeed))
    #
    #     # HI_current.append(windSimulationLillegrund._getCurrentHealthIndex())
    #     # HI_desired.append(windSimulationLillegrund._getDesiredHealthIndex())
    #     # timeVec.append(windSimulationLillegrund._getTimeIndex())
    #     # configurationVec.append(currentConfiguration[0])
    #
    #     plt.scatter(windSimulationLillegrund._getTimeIndex(), windSimulationLillegrund._getCurrentHealthIndex(),
    #                 label='HI current', color='r', s=20, marker=".")
    #     plt.scatter(windSimulationLillegrund._getTimeIndex(), windSimulationLillegrund._getDesiredHealthIndex(),
    #                 label='HI desired', color='k', s=20, marker=".")
    #     plt.draw()
    #     plt.pause(1e-20)


    # timeVecControllable = windSimulationLillegrund._getTimeVec()
    # desiredHealthIndexControllable = windSimulationLillegrund._getDesiredHealthIndexVec()
    # currentHealthIndexControllable = windSimulationLillegrund._getCurrentHealthIndexVec()
    # configurationControllable = windSimulationLillegrund._getCurrentConfigurationVec()
    #
    # plt.subplot(211)
    # plt.plot(timeVecControllable, desiredHealthIndexControllable, 'k--', label='HI_desired')
    # plt.plot(timeVecControllable, currentHealthIndexControllable, 'r--', label='HI_current')
    # plt.xlabel('DateTime Vector')
    # plt.ylabel('Health Index')
    # plt.legend(loc='upper right')
    # plt.grid()
    # #
    # plt.subplot(212)
    # plt.plot(timeVecControllable, configurationControllable, 'r--')
    # plt.xlabel('DateTime Vector')
    # plt.ylabel('Configuration')
    # plt.grid()
    # plt.show()
    #
    # end = time.time()
    # print('execution time: ', end - start)

    # =================================================================================================================
    # =========================================== Hourly; Daily; Weekly Update ========================================
    # =================================================================================================================

    # configurationControllable = []
    # global currentConfiguration
    # for windI, WindSpeed in enumerate(windSpeedVec_scada[1:]):
    #     otherInput = np.array(B_vals_scada[windI])
    #
    #     if windI % 6 == 0:
    #         deltaHI = windSimulationLillegrund._getDeltaHealthIndex()
    #         currentConfiguration = reliabilityControlTurbine.update(deltaHI, WindSpeed, otherInput)
    #         configurationControllable.append(currentConfiguration[0])
    #
    #     currentIncrement = windSimulationLillegrund.update(currentConfiguration, WindSpeed, otherInput)
    #
    #     desiredHealthIndexControllable = windSimulationLillegrund._getDesiredHealthIndexVec()
    #     currentHealthIndexControllable = windSimulationLillegrund._getCurrentHealthIndexVec()
    #     timeVec = windSimulationLillegrund._getTimeIndex()
    #
    #     print('Time: ' + dateTime[1:][windI])
    #
    # desiredHealthIndexControllable = windSimulationLillegrund._getDesiredHealthIndexVec()
    # currentHealthIndexControllable = windSimulationLillegrund._getCurrentHealthIndexVec()
    # timeVec = range(1, len(desiredHealthIndexControllable)+1, 1)
    #
    # plt.subplot(211)
    # plt.plot(timeVec, desiredHealthIndexControllable, 'k--', label='HI_desired')
    # plt.plot(timeVec, currentHealthIndexControllable, 'r--', label='HI_current')
    # plt.xlabel('DateTime Vector')
    # plt.ylabel('Health Index')
    # plt.legend(loc='upper right')
    # plt.grid()
    #
    # plt.subplot(212)
    # plt.plot(timeVec, configurationControllable, 'r--')
    # plt.xlabel('DateTime Vector')
    # plt.ylabel('Configuration')
    # plt.grid()
    # plt.show()
    #
    # end = time.time()
    # print('execution time: ', end - start)

    # =================================================================================================================
    # ============================== Real-time pyQtGraph plotting =====================================================
    # =================================================================================================================
    # Real-time pyQtGraph plotting

    app = QtGui.QApplication([])
    win = pg.GraphicsWindow(title="Update Health Index")
    p = win.addPlot(title="Real-time Health Index Plot")

    p.addLegend()
    p.showGrid(x=True, y=True, alpha=0.5)
    p.setLabels(bottom={'Time Vector'}, left={'Health Index'})

    curve1 = pg.ScatterPlotItem(pen='w')
    curve2 = pg.ScatterPlotItem(pen='r')

    # HI_des = deque()
    # HI_cur = deque()
    # T_vec = deque()

    def update():
        global curve1, curve2, HI_des, HI_cur
        for windI, WindSpeed in enumerate(windSpeedVec_scada[1:]):
            otherInput = np.array(B_vals_scada[windI])

            deltaHI = windSimulationLillegrund._getDeltaHealthIndex()
            currentConfiguration = reliabilityControlTurbine.update(deltaHI, WindSpeed, otherInput)
            windSimulationLillegrund.update(currentConfiguration, WindSpeed, otherInput)
            print('Time: ' + dateTime[1:][windI])

            # HI_des.append(float(windSimulationLillegrund._getCurrentHealthIndex()))
            # HI_cur.append(float(windSimulationLillegrund._getDesiredHealthIndex()))
            # T_vec.append(windSimulationLillegrund._getTimeIndex())

            curve1.addPoints(str(windSimulationLillegrund._getTimeIndex()), str(windSimulationLillegrund._getDesiredHealthIndex()))
            curve2.addPoints(str(windSimulationLillegrund._getTimeIndex()), str(windSimulationLillegrund._getCurrentHealthIndex()))

            p.addItem(curve1)
            p.addItem(curve2)

            QtGui.QGuiApplication.processEvents()
        # legend.setParentItem(curve1)
        # legend.setParentItem(curve2)

    update()
    pg.QtGui.QGuiApplication.exec_()
    end = time.time()
    print('execution time: ', end - start)

    # =================================================================================================================
    # ================================================================================================================
    # ================================================================================================================
    # =================================================================================================================

    # =================================================================================================================
    # =================================================================================================================

    # =================================================================================================================
    # =================================================================================================================














