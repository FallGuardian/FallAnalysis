import sys
import MySQLdb
import csv
import math
import numpy as np
import string
from time import time 
import pprint
from datetime import datetime
from package import *
##
## FallDetector
##
class FallDetector:
		
	## Every 10 line of string, write out string to file
	__writeOutConst = 10 

	## the number(smaple points number) and period(sec)of user observe  
	## to smartphone gyro and acc
	__dataObserveNum = 400
	__dataObserveTime = 4

	def __init__(self, cur, targerIdList):
		
		## Input BaseId for generate data and check
		self.targerIdList = targerIdList

		## Database link
		self.cur = cur

		## Database Structure and type (for SQL select)
		self.targetCols = ['base_id', 'id', 'acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z', 'label']
		self.targetTypes = ['i','i','f','f','f','f','f','f','i']

		## PathInfo
		self.basePath = "/home/youngcoma/Dropbox/newFallDetect/experiment"

	def preprocess(self):
		pass
	def test(self):

		label = dataManiplate.readTxtDataLabel(self.basePath,'125.txt')		
		print label
		# npData = dataManiplate.readTxtData(self.basePath,125)
		# datas = list(npData[:,0])
	def generateData(self):
		
		print 'Start to generate data~'
		for baseId in self.targerIdList:

			fw = open("{}/data/{}.txt".format(self.basePath, baseId) , 'w')
			
			datas = list(database.getTableColsById(self.cur, 'final_primitive_total', self.targetCols, baseId))
			
			## @@ Data Clean / Making Up / Denoise @@ ##
			dataManiplate.dataComplement(datas, baseId)	
			npDatas = np.array(datas, dtype=zip(self.targetCols, self.targetTypes))
			
			headerStr = "## Fall:{}\n## Format:SVM,TA,AV\n".format(npDatas[0]['label'])
			outputStr = ""
			outputStr+=headerStr
			for d in npDatas:

				## @@ SVM calculate @@ ##
				SVMvalue = dataManiplate.calSVM(d['acc_x'], d['acc_y'], d['acc_z'])

				## @@ SVM integal @@ ##
				# SVMintegral = dataManiplate.calSVMintegral( SVMColumn, dt )

				## @@ TA & TAdelta calculate @@ ##
				TAvalue = dataManiplate.calTA(d['acc_x'], d['acc_y'], d['acc_z'])

				## @@ AV & AVdelta calcalate @@ ##
				AVvalue = dataManiplate.calAV(d['acc_x'], d['acc_y'], d['acc_z'], d['gyro_x'], d['gyro_y'], d['gyro_z']) 

				## @@ POSTURE calcalate @@ ##
				
				outputStr += '{},{},{}\n'.format(SVMvalue, TAvalue, AVvalue)
			
			fw.write(outputStr)
		print 'Gnerating Completed~'
			# fw.close()
