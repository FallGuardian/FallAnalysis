##encode=UTF-8
import math
import numpy as np
import sys
import string

def dataComplement(datas, _id):

	for idx,d in enumerate(datas):
		# print "{}, {}".format(idx, val)
		if d[2] == 0 and d[3] == 0 and d[4] == 0 and\
			d[5] == 0 and d[6] == 0 and d[7] == 0:
			last = idx - 1
			# print '{} is broken at {}'.format(_id, last)
			datas[idx]=(datas[last][0],datas[last][1],datas[last][2],datas[last][3],datas[last][4],\
				datas[last][5],datas[last][6],datas[last][7],datas[last][8])

def lowPassFilter(dataList):
	return

def highPassFilter(acc_xList ,acc_yList ,acc_zList ,alpha):

	# direction of gravity vector depends on placing method of smartphone
	gX, gY, gZ = 0, -9.81, 0
	
	gX = alpha * gX + (1 - alpha) * acc_xList
	gY = alpha * gY + (1 - alpha) * acc_yList
	gZ = alpha * gZ + (1 - alpha) * acc_zList
	
	accX = acc_xList - gX
	accY = acc_yList - gY
	accZ = acc_zList - gZ

	return [accX, accY, accZ]

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
	
	# print rad2deg((gyro) * paraDict['dt'])
	

	## Raw Version
	# resultDict['angle'] += rad2deg(gyro*paraDict['dt'])
	return resultDict['angle']


def calPOSTURE(acc_x, acc_y, acc_z):
	Gref = [0,9.8,0]
	innerProduct = Gref[0]*acc_x+Gref[1]*acc_y+Gref[2]*acc_z
	grefLen = math.sqrt(pow(Gref[0],2)+pow(Gref[1],2)+pow(Gref[2],2))
	accLen = math.sqrt(pow(acc_x,2)+pow(acc_y,2)+pow(acc_z,2))
	return innerProduct*180/math.pi/(grefLen+accLen)

def calSVM( acc_x, acc_y, acc_z ):
	return math.sqrt(math.pow(acc_x,2)+math.pow(acc_y,2)+math.pow(acc_z,2))

def calSVMintegral( SVMColumn, dt ):

	previousSum = 0
	i = 1;
	for d in SVMColumn:
		previousSum = d*i*dt + previousSum
		# print d*i*dt 
	return previousSum
	
def calTA( acc_x, acc_y, acc_z):
	if acc_x != 0 and acc_y != 0 and acc_z != 0:
		return rad2deg(math.asin(acc_y/(math.sqrt(math.pow(acc_x,2)+math.pow(acc_y,2)+math.pow(acc_z,2)))))
	else:
		return 0

def calAV( acc_x, acc_y, acc_z , gyro_x, gyro_y, gyro_z):
	# Implem
	return abs(acc_x*math.sin(gyro_x)+acc_y*math.sin(gyro_y)-acc_z*math.cos(acc_y)*math.cos(acc_z))

def getGlobalMin(datas):
	return min(datas)

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
	
	if dataDict[int(_id)][3] > threasholdDict['AV'] and dataDict[int(_id)][2] < threasholdDict['TA'] \
		and dataDict[int(_id)][0] > threasholdDict['SVM']:
	# if dataDict[int(_id)][2] < threasholdDict['TA'] \
	# 	and dataDict[int(_id)][0] > threasholdDict['SVM']:
		## @@ non-fall check @@ ##
		# print dataDict[int(_id)]
		print "hit"
		if dataDict[int(_id)][-1] == 0:
			resultDict['errorCntFP']+=1
			resultDict['FPbaseIds'].append(str(_id))
			# if cnt > maxCnt and paraDict['maxCnt'] != -1:
			# 	overMaxCntCnt+=1
	else:
		
		if dataDict[int(_id)][-1] == 1:
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

def findSVMMaxMin(SVMColumn, baseId, label):
	maxValue = max(SVMColumn)
	minValue = min(SVMColumn)
	maxIndex = SVMColumn.index(maxValue)
	minIndex = SVMColumn.index(minValue)

	if maxIndex > minIndex:
		return {'maxValue':maxValue, 'maxIndex':maxIndex, \
		'minValue':minValue, 'minIndex':minIndex, 'baseId':baseId, 'label':label}
	else:
		pass
def findIndicesSVMminMaxWindow(dataSize, interval):

	## find window start, end index
	start, end, i = 0, 0, 0
	windowsIndex = []	
	while(True):
		# print i
		if end > dataSize - (interval/2):
			
			if dataSize%interval == 0:
				break

			start = dataSize - (interval/2)*2
			end = dataSize
			# print "{},{}".format(start,end)
			windowsIndex.append((start,end))
			break
		start = i * (interval/2)
		end = (i+1)*(interval/2)+(interval/2)
		# print "{},{}".format(start,end)
		windowsIndex.append((start,end))
		i+=1
	
	return windowsIndex

def overThresholdinWindows(SVMColumn, windowIndices,SVMminThreshold, SVMmaxThreshold):
	for i in windowIndices:
		start = i[0]
		end = i[1]		

		maxValue = max(SVMColumn[start:end])
		minValue = min(SVMColumn[start:end])
		maxIndex = SVMColumn[start:end].index(maxValue)
		minIndex = SVMColumn[start:end].index(minValue)

		if maxIndex > minIndex and maxValue > SVMmaxThreshold and minValue < SVMminThreshold:
			# print "minValue:{}, minValue:{}".format(minValue, maxValue)
			return True
		else: 
			return False

def SVMminMaxAlg(SVMColumn, label, baseId, SVMmin, SVMmax, resultDict):

	## find the SVM below SVMmin and index
	lowerSVMindices = [ SVMColumn.index(d) for d in filter(lambda x: x<SVMmin, SVMColumn) ]
	l = len(lowerSVMindices)
	# print "num:{}, min index:{}".format(l, max(lowerSVMindices))
	# print lowerSVMindices

	## find the SVM above SVMmax and index
	higherSVMindices = [ SVMColumn.index(d) for d in filter(lambda x: x>SVMmax, SVMColumn) ]
	h = len(higherSVMindices)
	# print "num:{}, max index:{}".format(h, min(higherSVMindices)) 
	# print higherSVMindices

	lSVMIdx, hSVMIdx = -1,-1
	if len(lowerSVMindices) != 0:
		lSVMIdx = max(lowerSVMindices)
	if len(higherSVMindices) != 0:
		hSVMIdx = min(higherSVMindices)
	
	if lSVMIdx != -1 and hSVMIdx != -1 and lSVMIdx < hSVMIdx:
		if label == 0:
			resultDict['errorCntFP']+=1
			resultDict['FPbaseIds'].append(str(baseId))
		else:
			resultDict['errorCntTN']+=1
			resultDict['TNbaseIds'].append(str(baseId))


def readTxtData(basePath, baseId):
	data = np.loadtxt("{}/data2/{}".format(basePath,baseId), delimiter=',')
	return data

def readTxtDataLabel(basePath, baseId):
	fp = open("{}/data2/{}".format(basePath, '{}'.format(baseId)), 'rb')
	label = fp.readline().split(':')[1].strip('\n')
	fp.close()
	return label

def readTxtConfig(basePath, configFileName):
	strList = []
	with open("{}/config/{}".format(basePath, configFileName), 'rb') as configFile:
		
		for line in configFile.readlines():
			
			if not line.startswith('#') :
				line = line.strip()
				strList.append(string.split(line,'='))
			
	# print 'Your experiment configs:\n{}\n\r'.format(strList)
	return dict(zip([row[0] for row in strList],[float(row[1]) for row in strList]))
	
