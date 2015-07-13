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
TAs = [dataManiplate.calTA(d['acc_x'], d['acc_y'], d['acc_z']) for d in npDatas]
SVMs = [dataManiplate.calSVM(d['acc_x'], d['acc_y'], d['acc_z']) for d in npDatas]
AVs = [dataManiplate.calAV(d['acc_x'], d['acc_y'], d['acc_z'], d['gyro_x'], d['gyro_z'], d['acc_z'],) for d in npDatas]

## @@ TA Making Up For  @@ ##

highBound = [max(TAs), max(SVMs)]
lowBound  = [min(TAs), min(SVMs)]
print 'TA max:{}, TA min:{}'.format(max(TAs), min(TAs))
print 'SVMs max:{}, SVMs min:{}'.format(max(SVMs), min(SVMs))

plt.grid(True)
plt.set_cmap(plt.cm.Paired)
plt.title('red:TA, blue:SVM, green:AV baseId %s'%(baseId))
plt.plot(range(len(TAs)), TAs, 'r', range(len(SVMs)), SVMs, 'b', range(len(AVs)), AVs, 'g')
plt.axis([0, 400, floor(min(lowBound)), ceil(max(highBound))])
plt.show()

cur.close();
