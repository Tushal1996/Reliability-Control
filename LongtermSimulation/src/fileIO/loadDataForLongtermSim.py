#! /usr/bin/env python
# -*- coding:utf-8 -*-


'''
Created on 02.09.2019

import scipy.io
import pandas as pd

def loadMatFileWithLookUpTables(filepath):
    lookUpTables=scipy.io.loadmat(filepath)
    del lookUpTables['__header__']
    del lookUpTables['__version__']
    del lookUpTables['__globals__']
    return lookUpTables

