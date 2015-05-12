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



## We can write fast filter for user profile 
fileName = '123.txt'
fw = open('/home/youngcoma/Dropbox/newFallDetect/experiment/input_id/{}'.format(fileName) , 'w')
allIds = database.getColDistinct(cur, 'final_base_id', 'base_id')
outputStr = "";
for base_id in allIds:
	outputStr+=str(base_id[0])+","

fw.write(outputStr)
fw.close()