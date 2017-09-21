import sys
import MySQLdb
from math import ceil, floor
import numpy as np
import mlpy
import matplotlib
import matplotlib.pyplot as plt
from package import *
from shutil import copyfile

db = database.initialize()
cur = db.cursor()
##	Describes: plot the


##	read target base_id to plot
if sys.argv[1] == 'all':
	targetIds = database.getColDistinct(cur, 'final_primitive_total', 'base_id')
else:
	targetIds = [sys.argv[1]]

targetCols = ['base_id', 'id', 'acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z', 'label']
targetTypes = ['i','i','f','f','f','f','f','f','i']
targetTable = 'final_primitive_total'
last = 0

for baseId in targetIds:
	
	print baseId
	datas = list(database.getTableColsById(cur, targetTable, targetCols, baseId))
	dataManiplate.dataComplement(datas, baseId)

	npDatas = np.array( datas, dtype=zip(targetCols,targetTypes))
	# print npDatas.shape
	TAs = [dataManiplate.calTA(d['acc_x'], d['acc_y'], d['acc_z']) for d in npDatas]
	SVMs = [dataManiplate.calSVM(d['acc_x'], d['acc_y'], d['acc_z']) for d in npDatas]
	AVs = [dataManiplate.calAV(d['acc_x'], d['acc_y'], d['acc_z'], d['gyro_x'], d['gyro_z'], d['acc_z'],) for d in npDatas]

	## @@ TA Making Up For  @@ ##

	# highBound = [max(TAs), max(SVMs)]
	# lowBound  = [min(TAs), min(SVMs)]
	highBound = [30]
	lowBound  = [min(SVMs)]
	# print 'TA max:{}, TA min:{}'.format(max(TAs), min(TAs))
	# print 'SVMs max:{}, SVMs min:{}'.format(max(SVMs), min(SVMs))

	plt.grid(True)
	plt.set_cmap(plt.cm.Paired)
	# plt.title('red:TA, blue:SVM, green:AV baseId %s'%(baseId))
	plt.title('blue:SVM baseId %s'%(baseId))
	# plt.title('blue:SVM baseId %s'%(baseId))
	# plt.plot(range(len(TAs)), TAs, 'r', range(len(SVMs)), SVMs, 'b', range(len(AVs)), AVs, 'g')
	plt.plot(range(len(SVMs)), SVMs, 'b')
	plt.axis([0, 350, floor(min(lowBound)), ceil(max(highBound))])
	# plt.show()

	figName = str(baseId)
	sourcePath = './experiment/figure/calculated/{}.png'.format(figName)
	dropboxPath = "/home/youngcoma/Dropbox/newFallDetect/experiment/figure/calculated/{}.png".format(figName)
	# dropboxPath = "/home/youngcoma/Dropbox/newFallDetect/experiment/figure/{}.png".format(figName)
	plt.savefig(sourcePath)
	plt.close()
		
	copyfile(sourcePath,dropboxPath)
	
cur.close();
