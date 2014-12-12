import sys
import MySQLdb
import csv
import math
import numpy as np
from time import time 
from datetime import datetime


# Customized database function & login info. in database.py
import database
import dataManiplate
cur = database.initialize()
fileName = ''


## @@ Script Input and Open File @@ ##
if len(sys.argv) == 2:
	if sys.argv[1] == '-h':
		print '''Usage: python dataGene [ReadFileName.csv], [OutputFileName.csv]
				ReadFileName.csv need to locate at folder /idSets/,
				OutputFileName.csv will generate at folder /data/, default name is datetime.'''
		# Reading the file from idSets
	else:
		try:
			fileName = sys.argv[1]
			targerIds = []
			with open("./idSets/{}".format(fileName), 'rb') as fp:
				reader = csv.reader(fp ,delimiter=',')
				for row in reader:
					targerIds.extend(row)
			pass
		except IOError as e:
			print "I/O error({0}): {1}".format(e.errno, e.strerror)
			raise
else:
	print '''not enough arugment, check help (keyin python dataGene -h'''


## @@ Write File to /data/ @@ ##
# t = time()
# fileName = datetime.fromtimestamp(t).strftime('%Y-%m-%d_%H:%M:%S')
fw = open('data/data_{}'.format(fileName) , 'w')

##
## Output Format [base_id][maxSVM][TAdelta][Avdelta][label]
##

# @@ Data Processing Setting @@ #
brokenList = ""
targetCols = ['base_id', 'id', 'acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z', 'label']
targetTypes = ['i','i','f','f','f','f','f','f','i']

## @@ Data Process From DataBase @@ ##
for _id in targerIds:
	
	print _id
	datas = list(database.getTableColsById(cur, 'lab_primitive2', targetCols, _id))
	
	
	## @@ Data Clean / Making Up / Denoise @@ ##
	if len(datas) != 400:
		print '{} is broken'.format(_id)
		last = len(datas) - 1
		appendData = map(tuple, (
				(0,0,datas[last][2],
				datas[last][3],
				datas[last][4],
				datas[last][5],
				datas[last][6],
				datas[last][7],0)
			for i in range(len(datas), 400)))
		datas = datas + appendData

	npDatas = np.array(datas, dtype=zip(targetCols,targetTypes))

	## @@ SVM calculate @@ ##
	maxSVM = -sys.maxint
	for d in npDatas:	
		maxSVM = max(maxSVM, dataManiplate.calSVM(d['acc_x'], d['acc_y'], d['acc_z']))

	## @@ TA & TAdelta calculate @@ ##
	TAinterval = 50
	TAdeltaMax = -sys.maxint
	TAColumn = [dataManiplate.calTA(d['acc_x'], d['acc_y'], d['acc_z']) for d in npDatas]

	for i in range(0,350):
		localMax = max(TAColumn[i:i+TAinterval])
		localMin = min(TAColumn[i:i+TAinterval])
		TAdeltaMax = max(localMax-localMin, TAdeltaMax)

	## @@ AV & AVdelta calcalate @@ ##
	AVinterval = 50
	AVdeltaMax = -sys.maxint
	AVColumn = [dataManiplate.calAV(d['acc_x'], d['acc_y'], d['acc_z'], d['gyro_x'], d['gyro_z'], d['acc_z'],) for d in npDatas]
	
	for i in range(0,350):
		localMax = max(AVColumn[i:i+AVinterval])
		localMin = min(AVColumn[i:i+AVinterval])
		AVdeltaMax = max(localMax-localMin, AVdeltaMax)
	
	## @@ Write Out to File @@ ##		
	outputStr ='{},{},{},{},{}\n'.format(_id, maxSVM, TAdeltaMax, AVdeltaMax, npDatas[0]['label'])
	fw.write(outputStr)
	# print outputStr

print 'mission completed'
fp.close()
fw.close()
# print 'Task completed!\n'
# print 'broken List: {}'.format(brokenList)