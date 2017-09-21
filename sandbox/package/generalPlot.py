#encoding=UTF-8
import sys
import MySQLdb
from math import ceil, floor
import numpy as np
import mlpy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from shutil import copyfile
from package import database, dataManiplate
	
def plotRaw(cur, baseId, targetCols, targetTypes, targetTable):
	
	datas = list(database.getTableColsById(cur, targetTable, targetCols, baseId))

	# dataManiplate.dataComplement(datas)

	npDatas = np.array( datas, dtype=zip(targetCols,targetTypes))
	# print npDatas.shape

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
	plt.suptitle ('red:x, blue:y, green:z (baseId:%s, upper:Acc, lower:Gryo)'%(baseId))

	plt.subplot(211)
	plt.plot([1, 2, 3])
	plt.plot(range(len(acc_x)), acc_x, 'r', range(len(acc_y)),\
	acc_y, 'b', range(len(acc_z)), acc_z, 'g')
	plt.axis([0, 400, -25, 25])


	plt.subplot(212)
	plt.plot(range(len(gyro_x)), gyro_x, 'r', range(len(gyro_y)),\
	gyro_y, 'b', range(len(gyro_z)), gyro_z, 'g')

	figName = str(baseId)
	sourcePath = './experiment/figure/raw/{}.png'.format(figName)
	dropboxPath = "/home/youngcoma/Dropbox/newFallDetect/experiment/figure/raw/{}.png".format(figName)
	plt.savefig(sourcePath)
	plt.close()
		
	copyfile(sourcePath,dropboxPath)

	
def plotSVMDistribution(_type, SVMData, Label, fileName):
	
	plt.set_cmap(plt.cm.Paired)
	fig1 = plt.figure(1)
	plt.grid(True)
	plt.title('SVM {} distribution'.format(_type))
	# print Label
	colors = ['r' if d == '1' else 'b' for d in Label]
	
	plot = plt.scatter(range(len(SVMData)), SVMData, c=colors)
	labx = plt.xlabel("baseId Series")
	laby = plt.ylabel("SVM")
	
	sourcePath = './experiment/figure/SVMmaxmin/{}.png'.format(fileName)
	dropboxPath = "/home/youngcoma/Dropbox/newFallDetect/experiment/figure/SVMmaxmin/{}_{}.png".format(fileName,_type)
	plt.savefig(sourcePath)
	plt.close()
		
# 	copyfile(sourcePath,dropboxPath)

# def plotSVMDistribution(SVMMinData, SVMMaxData, Label, fileName):
	
# 	plt.set_cmap(plt.cm.Paired)
# 	fig1 = plt.figure(1)
# 	plt.grid(True)
# 	plt.title('SVM distribution')
# 	# print Label
# 	colors = ['r' if d == '1' else 'b' for d in Label]

# 	plot = plt.scatter(SVMMinData, SVMMaxData, c=colors)
# 	labx = plt.xlabel("SVM min")
# 	laby = plt.ylabel("SVM max")
	
# 	sourcePath = './experiment/figure/SVMmaxmin/{}.png'.format(fileName)
# 	dropboxPath = "/home/youngcoma/Dropbox/newFallDetect/experiment/figure/SVMmaxmin/{}_minMax_Dist.png".format(fileName)
# 	plt.savefig(sourcePath)
# 	plt.close()
