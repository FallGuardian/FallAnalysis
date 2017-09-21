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
from package import *
db = database.initialize()
cur = db.cursor()
basePath = "/home/youngcoma/Dropbox/newFallDetect/experiment"

allBaseId = database.getColDistinct(cur, 'final_primitive_total','base_id')
targerIds = allBaseId

##
## Output Format [base_id][SVM][TA][AV][label]
##
## mode 1: Global Max
## mode 2: Local(50 intervals) Max Difference 
##	[SVM,TA,AV]

modeConfig = dataManiplate.readTxtConfig(basePath,'dataGeneMode.txt')
# @@ Data Processing Setting @@ #
targetCols = ['base_id', 'id', 'acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z', 'label']
targetTypes = ['i','i','f','f','f','f','f','f','i']

## @@ para setting in AV ##
dt = 6.0/400.0
alpha = 0.02
paraDict = {'alpha':alpha, 'dt':dt}

## @@ Data Process From DataBase @@ ##
for _id in targerIds:
	
	fw = open("{}/data2/{}.txt".format(basePath, str(_id)) , 'w')
	datas = list(database.getTableColsById(cur, 'final_primitive_total', targetCols, _id))
	# print "{}: len {}".format(_id, len(datas))
	
	## @@ Data Clean / Making Up / Denoise @@ ##
	dataManiplate.dataComplement(datas, _id)
	npDatas = np.array(datas, dtype=zip(targetCols,targetTypes))
	

	headerLabel = "##Fall:{}\n".format(npDatas[0]['label'])
	headerFormat = "##baseId, SVM, SVMintegral, TA, AV, POSTURE\n"
	
	outputStr = ""
	outputStr+=headerLabel
	outputStr+=headerFormat
	##
	## @@ SVM integal @@ ##
	##
	SVMColumn = [dataManiplate.calSVM(d['acc_x'], d['acc_y'], d['acc_z']) for d in npDatas]
	SVMintegral = dataManiplate.calSVMintegral( SVMColumn, dt )

	for d in npDatas:
		##
		## @@ SVM calculate @@ ##
		##
		SVM = dataManiplate.calSVM(d['acc_x'], d['acc_y'], d['acc_z'])
	
		##
		## @@ TA & TAdelta calculate @@ ##
		##
		TA = dataManiplate.calTA(d['acc_x'], d['acc_y'], d['acc_z'])

		##
		## @@ AV & AVdelta calcalate @@ ##
		##
		AV = dataManiplate.calAV(d['acc_x'], d['acc_y'], d['acc_z'], d['gyro_x'], d['gyro_y'], d['gyro_z']) 

		##
		## @@ POSTURE calcalate @@ ##
		##    using t
		##
		POSTURE = dataManiplate.calPOSTURE(d['acc_x'], d['acc_y'], d['acc_z'])

		##
		## @@ Write Out to File @@ ##		
		##
		# outputStr ='{},{},{},{},{}\n'.format(_id, SVM, TAdeltaMax, AVdeltaMax, npDatas[0]['label'])
		dataStr ='{},{},{},{},{},{}\n'.format(_id, SVM, SVMintegral, TA, AV, POSTURE)
		outputStr+=dataStr
	
	fw.write(outputStr)	
	outputStr = ""
	fw.close()
	# print 'Completed, {}'.format(outputName) 


print 'Task completed!\n'

