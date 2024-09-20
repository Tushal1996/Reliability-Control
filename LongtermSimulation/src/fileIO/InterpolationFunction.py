import pandas as pd
import numpy as np


def get_interpolation(a, p):

    # a: array with n dimensions
    # ranges: list of n lists or numpy arrays of values along each dimension
    # p: vector of values to find(n elements)

    # iterate through all dimensions

    wind_speed_range = list(range(4,34,2))
    b_value_range = list(range(-2,3,1))

    ranges = [wind_speed_range, b_value_range]

    for i in range(a.ndim):
        # check if we are out of range, if yes than use the last bounded values
        if p[i] <= ranges[i][0]:
            a = a[0]
            continue
        if p[i] >= ranges[i][-1]:
            a = a[-1]
            continue

        # find the nearest values
        right = np.searchsorted(ranges[i], p[i])
        left = right - 1

        # find the relative distance
        d = (p[i] - ranges[i][left]) / (ranges[i][right] - ranges[i][left])

        # calculate the interpolation
        a = (1 - d) * a[left] + d * a[right]
        # print('Interpolation: ', a)

    return a