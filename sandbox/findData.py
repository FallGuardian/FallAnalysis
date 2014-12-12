import numpy as np
import mlpy
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt 
import matplotlib.cm as cm

data = np.loadtxt('data.csv', delimiter=',')
baseIds, x, y = data[:, 0].astype(np.int),data[:, 1:4], data[:, 4].astype(np.int)
SVMmax, deltaTAmax, SVMSTD = data[:, 1], data[:, 2],data[:, 3]


print [int(row[0]) for row in data if row[1] < 16]