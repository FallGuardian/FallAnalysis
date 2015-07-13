import math
import numpy as np
import sys


def calVelocity( acc_x, acc_y, acc_z ):
	return (math.sqrt(math.pow(acc_x,2)+math.pow(acc_y,2)+math.pow(acc_z,2))-9.81)

def integrateAngle(acc1, acc2, gyro, paraDict, resultDict):
	# angleGyro = rad2deg(gyro*paraDict['dt']) 
	# # resultDict['angle'] += angleGyro
	# angleAcc = rad2deg(math.atan2(acc1, acc2))
	# # print angleAcc
	# resultDict['angle'] = (1-paraDict['alpha'])*angleGyro+\
	# paraDict['alpha']*angleAcc
	
	##
	angleAcc = rad2deg(math.atan2(acc1, acc2))
	resultDict['angle'] = (1-paraDict['alpha'])*(resultDict['angle'] + \
	rad2deg((gyro/65.536) * paraDict['dt'] )) + (paraDict['alpha'])*(angleAcc)
	
	print rad2deg((gyro) * paraDict['dt'])
	

	## Raw Version
	# resultDict['angle'] += rad2deg(gyro*paraDict['dt'])
	return resultDict['angle']


def calSVM( acc_x, acc_y, acc_z ):
	return math.sqrt(math.pow(acc_x,2)+math.pow(acc_y,2)+math.pow(acc_z,2))

def calSVMintegral( SVMColumn, dt ):

	previousSum = 0
	i = 0;
	for d in SVMColumn:
		i+=1
		previousSum = d*i*dt + previousSum
		print d*i*dt 
	return previousSum

def calTA( acc_x, acc_y, acc_z):
	if acc_x != 0 and acc_y != 0 and acc_z != 0:
		return rad2deg(math.asin(acc_y/(math.sqrt(math.pow(acc_x,2)+math.pow(acc_y,2)+math.pow(acc_z,2)))))
	else:
		return 0

def calAV( acc_x, acc_y, acc_z , gyro_x, gyro_y, gyro_z):
	# Implem
	return abs(acc_x*math.sin(gyro_x)+acc_y*math.sin(gyro_y)-acc_z*math.cos(acc_y)*math.cos(acc_z))


def getGlobalMax(datas):
	return max(datas)

def getLocalMaxDiffence(Column, interval):
	deltaMax = -sys.maxint
	for i in range(0,400-interval):
		localMax = max(Column[i:i+interval])
		localMin = min(Column[i:i+interval])
		deltaMax = max(localMax-localMin, deltaMax)
	return deltaMax

def rad2deg(rad):
	return rad*180.0/math.pi

def deg2rad(deg):
	return deg*math.pi/180.0

def findMaxCnt(cur, targerIds):
	
	maxCnt = 0
	for _id in targerIds:
		datas = list(database.getTableColsById(cur, targetTable, targetCols, _id))
		npDatas = np.array(datas, dtype=zip(targetCols,targetTypes))

		if npDatas[0]['label'] == 1:
			max(maxCnt, len(dataManiplate.findOverThreshold(npDatas, AV, SVM)))
	return maxCnt

def thresholdBaseAlg(dataDict, _id, threasholdDict, paraDict, resultDict):
	#@@ Cal SVM, TA @@##
	
	if dataDict[int(_id)][1] > threasholdDict['TA'] and	\
	dataDict[int(_id)][0] > threasholdDict['SVM']:
		## @@ non-fall check @@ ##
		if dataDict[int(_id)][3] == 0:
			resultDict['errorCntFP']+=1
			resultDict['FPbaseIds'].append(str(_id))
			# if cnt > maxCnt and paraDict['maxCnt'] != -1:
			# 	overMaxCntCnt+=1
	else:
		## @@ non-fall check @@ ##
		if dataDict[int(_id)][3] == 1:
			resultDict['errorCntTN']+=1
			resultDict['TNbaseIds'].append(str(_id))

def overThresholdCount(SVMColumn, TAColumn, AVColumn, threasholdDict):
	count = 0
	for i in range(0,400):

		# if SVMColumn[i] > threasholdDict['SVM'] and TAColumn[i] > threasholdDict['TA'] and \
		# AVColumn[i] > threasholdDict['AV'] :
		if SVMColumn[i] > threasholdDict['SVM'] :
			count+=1
	return count