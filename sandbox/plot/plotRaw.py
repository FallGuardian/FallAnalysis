import sys
import MySQLdb
from math import ceil, floor
import numpy as np
import mlpy
import matplotlib
import matplotlib.pyplot as plt
from pylab import *

import database
import dataManiplate
db = database.initialize()
cur = db.cursor()
##	Describes: plot the


##	read target base_id to plot
baseId = sys.argv[1]

targetCols = ['base_id', 'id', 'acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z', 'label']
targetTypes = ['i','i','f','f','f','f','f','f','i']
targetTable = 'final_primitive_total'

datas = list(database.getTableColsById(cur, targetTable, targetCols, baseId))
# print datas
if len(datas) != 400:
	print '{} is broken'.format(baseId)
	last = len(datas) - 1
	appendData = map(tuple, (
			(0,0,datas[last][2],
			datas[last][3],
			datas[last][4],
			datas[last][5],
			datas[last][6],
			datas[last][7],0)
		for i in range(len(datas), 400)))
	datas = datas + appendData

npDatas = np.array( datas, dtype=zip(targetCols,targetTypes))
print npDatas.shape

acc_x = [d['acc_x'] for d in npDatas]
acc_y = [d['acc_y'] for d in npDatas]
acc_z = [d['acc_z'] for d in npDatas]
gyro_x = [d['gyro_x'] for d in npDatas]
gyro_y = [d['gyro_y'] for d in npDatas]
gyro_z = [d['gyro_z'] for d in npDatas]

## @@ TA Making Up For  @@ ##


fig = plt.figure(1)
plt.grid(True)
plt.set_cmap(plt.cm.Paired)
plt.suptitle ('red:x, blue:y, green:z baseId:%s'%(baseId))

plt.subplot(211)

plt.plot(range(len(acc_x)), acc_x, 'r', range(len(acc_y)),\
 acc_y, 'b', range(len(acc_z)), acc_z, 'g')
# plt.axis([0, 400, -10, 15])


plt.subplot(212)

plt.plot(range(len(gyro_x)), gyro_x, 'r', range(len(gyro_y)),\
 gyro_y, 'b', range(len(gyro_z)), gyro_z, 'g')

basePath = "/home/youngcoma/Dropbox/newFallDetect/experiment"
figName = str(baseId)
plt.savefig("{}/figure/raw/{}.png".format(basePath,figName),bbox_inches='tight')
plt.show()

cur.close();
