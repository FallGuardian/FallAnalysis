import sys
import MySQLdb
from math import ceil, floor
import numpy as np
import mlpy
import matplotlib
import matplotlib.pyplot as plt
from package import *

db = database.initialize()
cur = db.cursor()

_id = sys.argv[1]

targetCols = ['base_id', 'id', 'acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z', 'label']
targetTypes = ['i','i','f','f','f','f','f','f','i']
datas = list(database.getTableColsById(cur, 'final_primitive_total', targetCols, _id))

# if len(datas) == 400:
# 	print '{} is broken'.format(_id)
# 	last = len(datas) - 1
# 	print last
# 	appendData = map(tuple, ( (0,0,datas[last][2],
# 			datas[last][3],
# 			datas[last][4],
# 			datas[last][5],
# 			datas[last][6],
# 			datas[last][7],0)for i in range(len(datas), 400)))
# 	print appendData
# 	datas = datas + appendData

npDatas = np.array(datas, dtype=zip(targetCols,targetTypes))

## @@ calculate Angle
resultDict = { 'angle':0 }
dt = 6.0/400.0
alpha = 0.02
paraDict = {'alpha':alpha, 'dt':dt}
pitchColunm = [dataManiplate.integrateAngle(d['acc_y'],d['acc_z'], d['gyro_x'], paraDict, resultDict) \
for d in npDatas]

## Plot angle 
basePath = "/home/youngcoma/Dropbox/newFallDetect/experiment"
figName = str(_id)
plt.grid(True)
plt.set_cmap(plt.cm.Paired)
plot = plt.plot(range(len(pitchColunm)), pitchColunm, 'g')
# plt.show()
plt.savefig("{}/figure/angle/{}.png".format(basePath,figName))
# print pitchColunm
