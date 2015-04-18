import numpy as np
import csv
from time import time 
from datetime import datetime
import database
import dataManiplate
import string

##	DESCRIBES: Use permutation and combination to find out the theashold to
##				optimize error
##	INPUT: config file, 
##
##


##
##	@@ Database initialization @@
##
db = database.initialize()
cur = db.cursor()

basePath = "/home/youngcoma/Dropbox/newFallDetect/experiment"

##
##	@@ OUTPUT: open write out file
##
writeOutFileName = 'test1_1.csv'
fw = open('{}/result/{}'.format(basePath, writeOutFileName) , 'w')
print 'Write out file name: {}'.format(writeOutFileName)

##
##	Read config/settings to set SVM,TA,AV from file
##
configFileName = 'settings.txt'
strList = []
with open("{}/config/{}".format(basePath, configFileName), 'rb') as configFile:
	
	for line in configFile.readlines():
		
		if not line.startswith('#') :
			line = line.strip()
			strList.append(string.split(line,'='))
		
print 'Your experiment configs:\n{}\n\r'.format(strList)
configsDict = dict(zip([row[0] for row in strList],[float(row[1]) for row in strList]))
# print configsDict
SVMstart, SVMend = configsDict['SVMstart'], configsDict['SVMend']                                  
TAstart ,TAend = configsDict['TAstart'], configsDict['TAend']
AVstart, AVend = configsDict['AVstart'], configsDict['AVend']
SVMstep, TAstep, AVstep = configsDict['SVMstep'], configsDict['TAstep'], configsDict['AVstep']


##
## @@ INPUT: read base_id from file @@ ##
##
# readFileName = 'test1.txt'
# targerIds = []
# with open("{}/input_id/{}".format(basePath, readFileName), 'rb') as fp:
# 	reader = csv.reader(fp ,delimiter=',')
# 	for row in reader:
# 		targerIds.extend(row)

# print 'Input base_id file: {}\n\r'.format(readFileName)


##
## @@ INPUT: read calculated_data from file @@ ##
##	dataDict Format: _id:{SVM, TA, AV, label} 
cal_dataFileName = 'test1_data.txt'
data = np.loadtxt("{}/calculated_data/{}".format(basePath,cal_dataFileName), delimiter=',')
base_id, attrs = data[:, 0].astype(np.int), data[:,1:5] 
dataDict = dict(zip(base_id, attrs))
# print 'calculated_data preview: \n{}\n\r'.format(dataDict)

targerIds = base_id
targetTable = 'final_primitive_total'
targetCols = ['base_id', 'id', 'acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z', 'label']
targetTypes = ['i','i','f','f','f','f','f','f','i']
totalCnt = len(base_id)

fw.write('#SVM,TA,AV,errorRate,FPids,TNids\n')

##
##	@@ Max Count enable/disable @@ ##
##	@@ set maxCnt = -1 can disable maxCnt function, otherwise enable
maxCnt = -1
# maxCnt = dataManiplate.findMaxCnt(cur, targerIds)
paraDict = {'maxCnt':maxCnt}

totalResultDict = {}

for SVM in np.arange(SVMstart, SVMend, SVMstep):
	for TA in np.arange(TAstart, TAend, TAstep):
		for AV in np.arange(AVstart, AVend, AVstep):
			
			# print 'SVM: {}, TA: {}, AV: {}'.format(SVM, TA, AV)
			# @@ Temperal varibale @@ ##
			threasholdDict = {'SVM':SVM, 'TA':TA, 'AV':AV}
			resultDict = {'errorCntFP':0,'errorCntTN':0,'overMaxCntCnt':0\
			,'FPbaseIds':[],'TNbaseIds':[]}

			for _id in targerIds:
				dataManiplate.thresholdBaseAlg(dataDict, _id, threasholdDict, paraDict, resultDict)

			# print resultDict		
			##	@@ calculate accurcy @@
			resultDict['errorRate'] = (resultDict['errorCntFP']+resultDict['errorCntTN']\
				-resultDict['overMaxCntCnt'])/ float(totalCnt)
			
			outputStr = '{},{},{},{},{}\n'.format( SVM, TA, AV, resultDict['errorRate']\
				, '+'.join(resultDict['FPbaseIds']), '+'.join(resultDict['TNbaseIds']) )
			# outputStr = '{},{},{},{},{}\n'.format( SVM, TA, AV, resultDict['errorRate']\
			# 	, resultDict['FPbaseIds'], resultDict['TNbaseIds'] )
			# outputStr = '{},{},{},{}\n'.format( SVM, TA, AV, resultDict['errorRate'])
			
			# print outputStr
			fw.write(outputStr)


fw.close()
print 'bruteForce2 completed, generate .csv file'
				## errorRate = (errorCntFP+errorCntTN-overMaxCntCnt)/totalCnt
