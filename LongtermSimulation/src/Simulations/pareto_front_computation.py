import pandas as pd
import numpy as np
import math
from scipy.io import savemat
import argparse
import sys
import matplotlib.pyplot as plt


def pareto_front(pareto_load, pareto_energy):

    # slope of a linear function
    slope = -((min(pareto_energy) - max(pareto_energy)) / (min(pareto_load) - max(pareto_load)))

    objective_values = list(zip(pareto_load, pareto_energy))
    alpha_current = []
    for x, y in objective_values:

        # Intersection points (f1_s, f2_s)
        f1_s = (max(pareto_energy) - y + ((x * (min(pareto_load) - max(pareto_load))) / (min(pareto_energy) - max(pareto_energy))) + (
                (min(pareto_load) * (min(pareto_energy) - max(pareto_energy))) / (min(pareto_load) - max(pareto_load)))) \
               / (((min(pareto_load) - max(pareto_load)) / (min(pareto_energy) - max(pareto_energy))) + ((min(pareto_energy) - max(pareto_energy)) / (min(pareto_load) - max(pareto_load))))

        f2_s = max(pareto_energy) + slope * (f1_s - min(pareto_load))

        # distances
        D_p = math.sqrt(((max(pareto_load) - min(pareto_load)) ** 2) + ((min(pareto_energy) - max(pareto_energy)) ** 2))

        D_a = math.sqrt(((max(pareto_load) - f1_s) ** 2) + ((min(pareto_energy) - f2_s) ** 2))

        # The current value of the alpha-parameterization
        alpha_cur = 1 - ((2 * D_a) / D_p)
        alpha_current.append(alpha_cur)

    return alpha_current


