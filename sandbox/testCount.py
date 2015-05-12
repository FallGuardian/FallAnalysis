#coding = utf8
import sys
import string
import numpy as np
import database
import csv
import dataManiplate

basePath = "/home/youngcoma/Dropbox/newFallDetect/experiment"

if len(sys.argv) == 2:
	if sys.argv[1] == '-h':
		print '''Usage: python dataGene [ReadFileName.csv]
				ReadFileName.csv need to locate at folder /experiment/input_id/,'''
		# Reading the file from idSets
	else:
		try:
			fileName = sys.argv[1]
			targerIds = []
			with open("{}/input_id/{}".format(basePath, fileName), 'rb') as fp:
				reader = csv.reader(fp ,delimiter=',')

				for row in reader:
					 for item in row:
					 	if item:
							targerIds.append(item)
			pass
		except IOError as e:
			print "I/O error({0}): {1}".format(e.errno, e.strerror)
			raise
else:
	print '''not enough arugment, check help (keyin python dataGene -h'''




##
##	input: testing AV, SVM, TA (this is user input selected optimal threshold)
##
configFileName = 'countSettings.txt'
strList = []
with open("{}/config/{}".format(basePath, configFileName), 'rb') as configFile:
	
	for line in configFile.readlines():
		
		if not line.startswith('#') :
			line = line.strip()
			strList.append(string.split(line,'='))
		
print 'Your experiment configs:\n{}\n\r'.format(strList)
configsDict = dict(zip([row[0] for row in strList],[float(row[1]) for row in strList]))

SVM = configsDict['SVM']
TA = configsDict['TA']
AV = configsDict['AV']
threasholdDict = {'SVM':SVM, 'TA':TA, 'AV':AV}

# for _id in targerIds:
# 	dataManiplate.thresholdBaseAlg(dataDict, _id, threasholdDict, paraDict, resultDict)
db = database.initialize()
cur = db.cursor()

targetCols = ['base_id', 'id', 'acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z', 'label']
targetTypes = ['i','i','f','f','f','f','f','f','i']


resultDict = {'errorCntFP':0,'errorCntTN':0,'overMaxCntCnt':0\
		,'FPbaseIds':[],'TNbaseIds':[]}

for _id in targerIds:
	
	datas = list(database.getTableColsById(cur, 'final_primitive_total', targetCols, _id))
	# print "{}: len {}".format(_id, len(datas))
	
	## @@ Data Clean / Making Up / Denoise @@ ##
	if len(datas) != 400:
		print '{} is broken'.format(_id)
		last = len(datas) - 1

		appendData = map(tuple, ( (0,0,datas[last][2],datas[last][3],datas[last][4],\
			datas[last][5],datas[last][6],datas[last][7],0)\
			for i in range(len(datas), 400)))
		
		datas = datas + appendData

	npDatas = np.array(datas, dtype=zip(targetCols,targetTypes))
	
	##
	## @@ SVM calculate @@ ##
	##
	SVMColumn = [dataManiplate.calSVM(d['acc_x'], d['acc_y'], d['acc_z']) for d in npDatas]
		
	
	##
	## @@ TA & TAdelta calculate @@ ##
	##
	TAColumn = [dataManiplate.calTA(d['acc_x'], d['acc_y'], d['acc_z']) for d in npDatas]


	##
	## @@ AV & AVdelta calcalate @@ ##
	##
	AVColumn = [dataManiplate.calAV(d['acc_x'], d['acc_y'], d['acc_z'], d['gyro_x'], d['gyro_y'], d['gyro_z']) for d in npDatas]
	
	##
	##	find MaxCount
	##
	maxCnt = 0
	# if npDatas[0]['label'] == 1:
	# 	maxCnt = max(maxCnt, dataManiplate.overThresholdCount(SVMColumn,TAColumn,AVColumn,threasholdDict)) 
	overCount = dataManiplate.overThresholdCount(SVMColumn,TAColumn,AVColumn,threasholdDict)
	print "base_id:{}, overCount:{}, fall={}".format(npDatas[0]['base_id'],overCount,npDatas[0]['label'])
	


# database.getOverThresholdCount(cur, threasholdDict, 'final_primitive_total', 'SVM')