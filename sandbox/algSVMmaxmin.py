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


##
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




windowIndices = []
## Get the Windows start, end index
for baseId in targetIds:
	label = dataManiplate.readTxtDataLabel(basePath, "{}.txt".format(str(baseId)))
	npData = dataManiplate.readTxtData(basePath, "{}.txt".format(str(baseId)))
	SVMColumn = list(npData[:,0])
	windowIndices = dataManiplate.findIndicesSVMminMaxWindow(len(SVMColumn),150)
	break


total = len (targetIds)
SVMminThreshold, SVMmaxThreshold = 5,15
validateCnt,validateList = 0, []
hitCnt, hitList = 0, []
errorCnt, errorList = 0, []
FPCnt, FPList = 0, []
FNCnt, FNList = 0, []

for baseId in targetIds:
	label = dataManiplate.readTxtDataLabel(basePath, "{}.txt".format(str(baseId)))
	npData = dataManiplate.readTxtData(basePath, "{}.txt".format(str(baseId)))
	SVMColumn = list(npData[:,0])
	label = int(label)
	if dataManiplate.overThresholdinWindows(SVMColumn, windowIndices, SVMminThreshold, SVMmaxThreshold):
		# print "baseId:{}, label:{}".format(baseId,label)
		hitCnt+=1
		hitList.append(baseId)
		if label == 1:
			validateCnt+=1
			validateList.append(baseId)
		else:
			errorCnt+=1
			errorList.append(baseId)
	else:
		
		if label == 1:
			FPCnt+=1
			FPList.append(baseId)
		else:
			FNCnt+=1
			FNList.append(baseId)

		# print SVMColumn[start:end]
		# dataManiplate.SVMminMaxAlg(SVMColumn[start:end], label, baseId, SVMminThreshold, SVMmaxThreshold, resultDict)
		# print dataManiplate.findSVMMaxMin(SVMColumn[start:end],baseId,label)

errorRate = (errorCnt+FPCnt)/float(total)
print "errorRate: {}/{}={}".format((errorCnt+FPCnt), total, errorRate )
print "errorCnt: {}, errorList: {}".format(errorCnt, errorList)
print "FPCnt:{}, FPList: {}".format(FPCnt,FPList)



## Test Order of Max, min
# orderCnt = 0 
# totalCnt = len(targetIds)	
# baseIdMaxMinList = []
# for baseId in targetIds:
# 	label = dataManiplate.readTxtDataLabel(basePath, "{}.txt".format(str(baseId)))
# 	npData = dataManiplate.readTxtData(basePath, "{}.txt".format(str(baseId)))
# 	SVMColumn = list(npData[:,0])
# 	maxValue = max(SVMColumn)
# 	minValue = min(SVMColumn)
# 	maxIndxe = SVMColumn.index(maxValue) 
# 	minIndex = SVMColumn.index(minValue)
# 	if minIndex < maxIndxe:
# 		baseIdMaxMinList.append([baseId,label,minValue,maxValue])
# 		orderCnt+=1

# print 'right order/total: {}/{}'.format(orderCnt,totalCnt)

# nonFallCnt = 0
# for d in baseIdMaxMinList:
# 	if d[1] == '0':
# 		nonFallCnt+=1
# print "nonFallCnt/right order: {}/{}".format(nonFallCnt, orderCnt)
# 	maxMinData = dataManiplate.findSVMMaxMin(SVMColumn, baseId, label)
# 	if maxMinData:
# 		baseIdMaxMinList.append(maxMinData)

# SVMMaxData = [d['maxValue']for d in baseIdMaxMinList]
# SVMMinData = [d['minValue']for d in baseIdMaxMinList]
# BaseIdLabel = [d['label']for d in baseIdMaxMinList]


# # generalPlot.plotSVMDistribution('Min', SVMMinData, BaseIdLabel, fileName)
# # generalPlot.plotSVMDistribution('Max', SVMMaxData, BaseIdLabel, fileName)
# print fileName
# generalPlot.plotSVMDistribution(SVMMinData, SVMMaxData, BaseIdLabel, fileName)

print "finish at {}".format(str(datetime.now()))

