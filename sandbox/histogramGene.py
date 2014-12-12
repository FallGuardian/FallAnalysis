import numpy as np
import csv
import timeit
# Customized database function & login info. in database.py
import database
import dataManiplate
cur = database.initialize()

##
## Using static pre-analyze Method
## 

startTime = timeit.default_timer()

targetCols = ['base_id', 'id', 'acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z', 'label']
targetTypes = ['i','i','f','f','f','f','f','f','i']

## @@ set TA, SVM, AV init @@ ##
TAstep, SVMstep, AVstep, TAdelta, AVdelta = 1, 0.1, 0.1, 1, 0.1

TAstart ,TAend = -80,95
SVMstart, SVMend = 0,35
AVstart, AVend = 0,35

TAdeltaStart, TAdeltaEnd = 0,175
AVdeltaStart, AVdeltaEnd = 0, 45


# @@ for all id loop @@ ##
targerIds = []
with open("./idSets/all_549.csv", 'rb') as fp:
	reader = csv.reader(fp ,delimiter=',')
	for row in reader:
		targerIds.extend(row)

# fw = open('./histogram/TA.hist', 'w')
# for TA in np.arange(TAstart, TAend, TAstep):
# 	overIds = []
# 	for _id in targerIds:
		
# 		datas = list(database.getTableColsById(cur, 'lab_primitive2', targetCols, _id))
# 		npDatas = np.array(datas, dtype=zip(targetCols,targetTypes))
		
# 		if len([d['id']for d in npDatas if dataManiplate.calTA(d['acc_x'], d['acc_y'], d['acc_z'])>TA])> 0:
# 			overIds.append(_id)

# 	outputStr = '{}|{}\n'.format(TA,','.join(overIds))
# 	print TA
# 	fw.write(outputStr)
# fw.close()

# fw2 = open('./histogram/SVM.hist', 'w')
# for SVM in np.arange(SVMstart, SVMend, SVMstep):
# 	overIds = []
# 	for _id in targerIds:
		
# 		datas = list(database.getTableColsById(cur, 'lab_primitive2', targetCols, _id))
# 		npDatas = np.array(datas, dtype=zip(targetCols,targetTypes))
		
# 		if len([d['id']for d in npDatas if dataManiplate.calSVM(d['acc_x'], d['acc_y'], d['acc_z'])>SVM])> 0:
# 			overIds.append(_id)

# 	outputStr = '{}|{}\n'.format(SVM,','.join(overIds))
# 	print SVM
# 	fw2.write(outputStr)
# fw2.close()

fw3 = open('./histogram/AV.hist', 'w')
for AV in np.arange(AVstart, AVend, AVstep):
	overIds = []
	for _id in targerIds:
		
		datas = list(database.getTableColsById(cur, 'lab_primitive2', targetCols, _id))
		npDatas = np.array(datas, dtype=zip(targetCols,targetTypes))
		
		if len([d['id']for d in npDatas if dataManiplate.calAV(d['acc_x'], d['acc_y'], d['acc_z'],d['gyro_x'], d['gyro_y'], d['gyro_z'])>AV])> 0:
			overIds.append(_id)

	outputStr = '{}|{}\n'.format(AV,','.join(overIds))
	print AV
	fw3.write(outputStr)
fw3.close()



endTime = timeit.default_timer()
print 'histogram generation completed, cost {} sec'.format(endTime-startTime)