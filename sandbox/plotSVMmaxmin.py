# coding=UTF-8
import numpy as np
import csv
from time import time 
from datetime import datetime
from package import *
import string
import sys
import operator
from datetime import datetime
from collections import namedtuple
#
##	@@ Database initialization @@
##
db = database.initialize()
cur = db.cursor()

targetCols = ['base_id', 'id', 'acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z', 'label']
targetTypes = ['i','i','f','f','f','f','f','f','i']

##
## @@ INPUT: read calculated_data from file @@ ##
##	dataDict Format: _id:{SVM, TA, AV, label} 
##

basePath = "/home/youngcoma/Dropbox/newFallDetect/experiment"
targetIds = []
if sys.argv[1] == 'all':
	targetIds = database.getColDistinct(cur, 'final_primitive_total', 'base_id')
else:
	fileName = sys.argv[1]
	with open("{}/input_id/{}".format(basePath, fileName), 'rb') as fp:
		reader = csv.reader(fp ,delimiter=',')
		for row in reader:
			 for item in row:
			 	if item:
					targetIds.append(item)


# Test Order of Max, min
orderCnt = 0 
totalCnt = len(targetIds)	
baseIdMaxMinList = []
for baseId in targetIds:
	label = dataManiplate.readTxtDataLabel(basePath, "{}.txt".format(str(baseId)))
	npData = dataManiplate.readTxtData(basePath, "{}.txt".format(str(baseId)))
	SVMColumn = list(npData[:,0])
	maxValue = max(SVMColumn)
	minValue = min(SVMColumn)
	maxIndxe = SVMColumn.index(maxValue) 
	minIndex = SVMColumn.index(minValue)
	maxMinData = dataManiplate.findSVMMaxMin(SVMColumn, baseId, label)
	baseIdMaxMinList.append(maxMinData)
	# if minIndex < maxIndxe:
	# 	baseIdMaxMinList.append([baseId,label,minValue,maxValue])
	# 	orderCnt+=1

print 'right order/total: {}/{}'.format(orderCnt,totalCnt)
print baseIdMaxMinList
nonFallCnt = 0
# for d in baseIdMaxMinList:
	# if d[1] == '0':
	# 	nonFallCnt+=1
# print "nonFallCnt/right order: {}/{}".format(nonFallCnt, orderCnt)
	# if maxMinData:
		# baseIdMaxMinList.append(maxMinData)

SVMMaxData = [d['maxValue']for d in baseIdMaxMinList]
SVMMinData = [d['minValue']for d in baseIdMaxMinList]
BaseIdLabel = [d['label']for d in baseIdMaxMinList]


# generalPlot.plotSVMDistribution('Min', SVMMinData, BaseIdLabel, fileName)
# generalPlot.plotSVMDistribution('Max', SVMMaxData, BaseIdLabel, fileName)
# print fileName
# generalPlot.plotSVMDistribution(SVMMinData, SVMMaxData, BaseIdLabel, fileName)