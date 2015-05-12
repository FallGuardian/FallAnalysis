import sys
import MySQLdb
import csv
import math
import numpy as np
import string
from time import time 
from datetime import datetime


##
##	Describes: This script calculates alg. method and generate data (caled_data) for testing accuracy
##
##	Usage: python dataGene.py idFile
##	
##	Input: file contained id (A) at /input_id/
##
##	Ouptut:  calculated data SVM,TA...etc (A_data) at /calculated_data/
##

##
##	@@ Database initialization @@
##
import database
import dataManiplate
db = database.initialize()
cur = db.cursor()
fileName = ''
basePath = "/home/youngcoma/Dropbox/newFallDetect/experiment"

## @@ Script Input and Open File @@ ##
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


## @@ Write File to /data/ @@ ##
# t = time()
# dt = datetime.fromtimestamp(t).strftime('%Y-%m-%d__%H_%M_%S')
nameSeg = string.split(fileName,'.')
outputName =  "{}_data.txt".format(nameSeg[0])

fw = open("{}/calculated_data/{}".format(basePath, outputName) , 'w')

##
## Output Format [base_id][SVM][TA][AV][label]
##
## mode 1: Global Max
## mode 2: Local(50 intervals) Max Difference 
##	[SVM,TA,AV]
mode=[1,1,1]

# @@ Data Processing Setting @@ #
brokenList = ""
targetCols = ['base_id', 'id', 'acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z', 'label']
targetTypes = ['i','i','f','f','f','f','f','f','i']

## @@ para setting in AV ##
dt = 6.0/400.0
alpha = 0.02
paraDict = {'alpha':alpha, 'dt':dt}

## @@ Data Process From DataBase @@ ##
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

	if mode[0] == 1:
		SVM = dataManiplate.getGlobalMax(SVMColumn)
	elif mode[0] == 2:
		SVMinterval = 50	
		SVM = dataManiplate.getLocalMaxDiffence(SVMColumn, SVMinterval)
	
	##
	## @@ TA & TAdelta calculate @@ ##
	##
	TAColumn = [dataManiplate.calTA(d['acc_x'], d['acc_y'], d['acc_z']) for d in npDatas]
	if mode[0] == 1:
		TA = dataManiplate.getGlobalMax(TAColumn)
	elif mode[0] == 2:
		TAinterval = 50
		TA = dataManiplate.getLocalMaxDiffence(TAColumn, TAinterval)

	##
	## @@ AV & AVdelta calcalate @@ ##
	##
	AVColumn = [dataManiplate.calAV(d['acc_x'], d['acc_y'], d['acc_z'], d['gyro_x'], d['gyro_y'], d['gyro_z']) for d in npDatas]
	if mode[0] == 1:
		AV = dataManiplate.getGlobalMax(AVColumn)
	elif mode[0] == 2:
		AVinterval = 50
		AV = dataManiplate.getLocalMaxDiffence(AVColumn, AVinterval)

	# dataManiplate.integrateAngle()

	##
	## @@ Write Out to File @@ ##		
	##
	# outputStr ='{},{},{},{},{}\n'.format(_id, SVM, TAdeltaMax, AVdeltaMax, npDatas[0]['label'])
	outputStr ='{},{},{},{},{}\n'.format(_id, SVM, TA, AV, npDatas[0]['label'])
	
	# print outputStr
	fw.write(outputStr)

print 'dataGene completed, {}'.format(outputName) 

fp.close()
fw.close()
print 'Task completed!\n'
print 'broken List: {}'.format(brokenList)
