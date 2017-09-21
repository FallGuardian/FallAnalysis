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

##
##	Read data 
##

if len(sys.argv) == 2:
	if sys.argv[1] == '-h':
		print '''Usage: python bruteForce2 [data.txt]
				ReadFileName.csv need to locate at folder /experiment/calculated_data/,'''
		# Reading the file from idSets
	else:
		try:
			fileName = string.split(sys.argv[1])
			print fileName[0]
			# targerIds = []
			# with open("{}/input_id/{}".format(basePath, fileName), 'rb') as fp:
			# 	reader = csv.reader(fp ,delimiter=',')
			# 	for row in reader:
			# 		targerIds.extend(row)
			# pass
		except IOError as e:
			print "I/O error({0}): {1}".format(e.errno, e.strerror)
			raise
else:
	print '''not enough arugment, check help (keyin python bruteForce2 -h'''


basePath = "/home/youngcoma/Dropbox/newFallDetect/experiment"

##
## @@ INPUT: read calculated_data from file @@ ##
##	dataDict Format: _id:{SVM, TA, AV, label} 
##
cal_dataFileName = fileName[0]
data = np.loadtxt("{}/calculated_data/{}".format(basePath,cal_dataFileName), delimiter=',')
base_id, attrs = data[:, 0].astype(np.int), data[:,1:6] 
dataDict = dict(zip(base_id, attrs))

# print 'calculated_data preview: \n{}\n\r'.format(dataDict)

targerIds = base_id
# targetTable = 'final_primitive_total'
# targetCols = ['base_id', 'id', 'acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z', 'label']
# targetTypes = ['i','i','f','f','f','f','f','f','i']
totalCnt = len(base_id)


##
##	Read config/settings to set SVM,TA,AV from file
##
configsDict = dataManiplate.readTxtConfig(basePath, 'settings.txt')
print configsDict

##
##	@@ OUTPUT: open write out file
##
writeOutFileName = '{}_result.csv'.format(string.split(cal_dataFileName,'.')[0])
fw = open('{}/result/{}'.format(basePath, writeOutFileName) , 'w')
print 'Write out file name: {}'.format(writeOutFileName)
# fw.write('#SVM,TA,AV,errorRate,FPids,TNids\n')

##
##	@@ Max Count enable/disable @@ ##
##	@@ set maxCnt = -1 can disable maxCnt function, otherwise enable
maxCnt = -1
# maxCnt = dataManiplate.findMaxCnt(cur, targerIds)
paraDict = {'maxCnt':maxCnt}

totalErrorRate = {}
totalFPbaseIds = {}
totalTNbaseIds = {}
paraKeys = namedtuple("paraKeys", ["SVM", "TA", "AV"])

print "Start Time:{}".format(str(datetime.now()))

for SVM in np.arange(configsDict['SVMstart'], configsDict['SVMend'], configsDict['SVMstep']):
	for TA in np.arange(configsDict['TAstart'], configsDict['TAend'], configsDict['TAstep']):
		for AV in np.arange(configsDict['AVstart'], configsDict['AVend'], configsDict['AVstep']):
			
			# print 'SVM: {}, TA: {}, AV: {}'.format(SVM, TA, AV)
			# @@ Temperal varibale @@ ##
			threasholdDict = {'SVM':SVM, 'TA':TA, 'AV':AV}
			resultDict = {'errorCntFP':0,'errorCntTN':0,'overMaxCntCnt':0\
			,'FPbaseIds':[],'TNbaseIds':[]}

			for _id in targerIds:
				dataManiplate.thresholdBaseAlg(dataDict, _id, threasholdDict, paraDict, resultDict)

			
			##	@@ calculate accurcy @@

			resultDict['errorRate'] = (resultDict['errorCntFP']+resultDict['errorCntTN']\
				-resultDict['overMaxCntCnt'])/ float(totalCnt)
			
			
			# print 'SVM:{},TA:{},AV:{},error:{}\n'.format( SVM, TA, AV, resultDict['errorRate'])

			
			k = paraKeys(SVM=SVM, TA=TA, AV=AV)
			totalErrorRate.update({k:resultDict['errorRate']})
			totalFPbaseIds.update({k:'+'.join(resultDict['FPbaseIds'])})
			totalTNbaseIds.update({k:'+'.join(resultDict['TNbaseIds'])})


## Write to File by increasing order

min_val = min(totalErrorRate.itervalues())
for SVM in np.arange(configsDict['SVMstart'], configsDict['SVMend'], configsDict['SVMstep']):
	for TA in np.arange(configsDict['TAstart'], configsDict['TAend'], configsDict['TAstep']):
		for AV in np.arange(configsDict['AVstart'], configsDict['AVend'], configsDict['AVstep']):
			if totalErrorRate[paraKeys(SVM,TA,AV)] == min_val:
				outputStr = "{},{},{},{},{},{}\n".format(SVM,TA,AV,totalErrorRate[paraKeys(SVM,TA,AV)]\
					,totalFPbaseIds[paraKeys(SVM,TA,AV)],totalTNbaseIds[paraKeys(SVM,TA,AV)]) 
				fw.write(outputStr)
print "Finish Time:{}".format(str(datetime.now()))
fw.close()
# print 'bruteForce2 completed, generate .csv file'
				# errorRate = (errorCntFP+errorCntTN-overMaxCntCnt)/totalCnt
