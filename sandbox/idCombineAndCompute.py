# encoding: utf-8
#!/usr/bin/python
import numpy as np
import csv
from time import time 
from datetime import datetime
# Customized database function & login info. in database.py
import database
import dataManiplate
db = database.initialize()
cur = db.cursor()

## @@ set TA, SVM, AV init @@ ##
TAstart ,TAend = 0,40
SVMstart, SVMend = 15,30
AVstart, AVend = 10,30
TAstep, SVMstep, AVstep = 1, 0.1, 1

## @@ id Setting @@ ##
targetCols = ['base_id', 'id', 'acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z', 'label']
targetTypes = ['i','i','f','f','f','f','f','f','i']

targerIds = list(database.getColDistinct( cur, 'final_primitive_0', 'base_id'))
targetIds2 = list(database.getColDistinct( cur, 'final_primitive_1','base_id'))

database.insertNewId(db, 100, 100)
## @@ SELECT OLD DATA @@ ##
inputTable = 'final_primitive_1'
primitive_1_base_id = database.getColDistinct(cur, inputTable, 'base_id')
for base_id in primitive_1_base_id: 
	print base_id[0]
	for data,i in zip(database.getTableRowsByColValue(cur,inputTable,'base_id',base_id[0]),range(1,401)):
		# new_base_id = data[0]-1484
		# new_id = (data[0]-1484)*400+i
		# tuple1 = (new_base_id,new_id)
		tuple2 = (data[0],)
		# newData = tuple1+data[2:15]+tuple2
		newData = data[0:15]+tuple2
		# print newData
		database.insertPrimitive(db, newData)
	


# # @@ test all unit function about physcial calculation @@
# base_id = 1284
# gyroX, gyroY, gyroZ = ['gyro_x'], ['gyro_y'], ['gyro_z']
# gyroType = ['f']

# gyroXData = list(database.getTableColsById(cur, 'final_primitive', gyroX, base_id))
# gyroXCumulation = dataManiplate.calGyroCumulation( gyroXData)

# gyroYData = list(database.getTableColsById(cur, 'final_primitive', gyroY, base_id))
# gyroYCumulation = dataManiplate.calGyroCumulation( gyroYData)

# gyroZData = list(database.getTableColsById(cur, 'final_primitive', gyroZ, base_id))
# gyroZCumulation = dataManiplate.calGyroCumulation( gyroZData)


# SampleNum = 400 # 400 sample point in an event
# period = 3 # 3 sec
# print gyroZCumulation * period/SampleNum
# print gyroYCumulation * period/SampleNum
# print gyroXCumulation * period/SampleNum
# 

	# print theda*(timePeriod/N)**2


# @@ Calculate test_primitive physical property @@
# listTestData = list(database.getTableAll(cur, 'test_primitive'))
# testData = zip([item[0] for item in listTestData], listTestData)
# print testData[0]
# @@ Calculate final_primitive physical property @@

# @@ Write to file @@
# allIds = targerIds + targetIds2
# for oldBase_id in allIds:
# 	print oldBase_id

# targerIds = [508,509,512,513,514,515,516,517,529,530,531,533,534,536,551,552,553,537,538,539,540,542,543,544,545,546,547,548,549]

# t = time()
# fileName = datetime.fromtimestamp(t).strftime('%Y-%m-%d_%H:%M:%S')
# fileName='all_data.csv'
# fw = open('/home/youngcoma/Dropbox/newfallDetect/data/{}'.format(fileName) , 'a+')

## @@ Table Header @@ ##
# fw.write('new_base_id, old_base_id, id, SVM, TA, AV, V')
# totalCnt = len(targerIds)
# totalCnt = len(targerIds)
# for SVM in np.arange(SVMstart, SVMend, SVMstep):
# 	for AV in np.arange(AVstart, AVend, AVstep):
# 		# for TA in np.arange(TAstart, TAend, TAstep):

# 		## @@ find Max Count @@ ##
# 		maxCnt = 0
# 		for _id in targerIds:
# 			datas = list(database.getTableColsById(cur, 'lab_primitive2', targetCols, _id))
# 			npDatas = np.array(datas, dtype=zip(targetCols,targetTypes))

# 			if npDatas[0]['label'] == 1:
# 				maxCnt = max(maxCnt, len(dataManiplate.findOverThreshold(npDatas, AV, SVM)))

# 		## @@ Find Treahold @@ ##
# 		errorCntFP = 0
# 		errorCntTN = 0
# 		overMaxCntCnt = 0
# 		FPbaseIds = []
# 		TNbaseIds = []

# 		for _id in targerIds:

# 			## @@ 400 per base_id data @@ ##
# 			datas = list(database.getTableColsById(cur, 'lab_primitive2', targetCols, _id))
# 			npDatas = np.array(datas, dtype=zip(targetCols,targetTypes))
			

# 			##@@ Cal  TA, SVM, AV @@##
# 			cnt = len(dataManiplate.findOverThreshold(npDatas, AV, SVM))
# 			if cnt > 0:
# 				## @@ non-fall check @@ ##
# 				if npDatas[0]['label'] == -1:
# 					errorCntFP+=1
# 					FPbaseIds.append(npDatas[0]['base_id'])
					
# 					if cnt > maxCnt:
# 						overMaxCntCnt+=1
# 			else:
# 				## @@ non-fall check @@ ##
# 				if npDatas[0]['label'] == 1:
# 					errorCntTN+=1
# 					TNbaseIds.append(npDatas[0]['base_id'])
			
# 		## @@  Enable / Disable MaxCount => deduce overMaxCntCnt @@ ##
# 		errorRate = (errorCntFP+errorCntTN)/ float(totalCnt)
# 		outputStr = '{},{},{},{},{}\n'.format('0', SVM, AV, errorRate, FPbaseIds, TNbaseIds)
# 		fw.write(outputStr)


# fw.close()
print 'completed'
				## errorRate = (errorCntFP+errorCntTN-overMaxCntCnt)/totalCnt
