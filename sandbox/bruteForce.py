import numpy as np
import csv
from time import time 
from datetime import datetime
# Customized database function & login info. in database.py
import database
import dataManiplate
cur = database.initialize()

targetCols = ['base_id', 'id', 'acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z', 'label']
targetTypes = ['i','i','f','f','f','f','f','f','i']



## @@ set TA, SVM, AV init @@ ##
TAstart ,TAend = 0,40
SVMstart, SVMend = 15,30
AVstart, AVend = 10,30
TAstep, SVMstep, AVstep = 1, 0.1, 1

## @@ id Setting @@ ##
##targerIds = [398,397,396,399,400,598,404,405,406,408,409,599,413,416,417,418,419,368,374,375,592,590,591,596,597,587,588,589,584,585,586,608,612,615,619,610,614,618,609,613,617,620,622,624,626,627,628,629,631,632,633,634,1142,1143,1144,1139,1140,1141,1133,1134,1135,1136,1137,1138,1145,1146,1147,1148,1149,1150,1163,1158,1162,1161,1152,1155,1157,1151,1154,1156,1114,1115,1116,1117,1118,1119,1120,1121,1123,1125,1126,1127,1129,1131,1132,1111,1112,1113,1092,1093,1094,1095,1097,1098,1099,1101,1102,1104,1106,1108,1110,1105,1107,1109,837,840,841,851,852,853,847,848,849,842,843,845,831,832,836,817,818,819,820,821,823,880,881,882,884,885,886 ,824,828,829,1276,1277,1278,1279,1280,1202,1203,1204,1205,1211,1212,1213,1206,1207,1209,1216,1218,1219,1200,1201,890,891,892,1261,1262,1263,1272,1273,1274,1225,1227,1228,1222,1223,1224,1235,1236,1240,1232,1231,1233,1248,1249,1250,893,894,895,1265,1267,1269,1270,1271,1258,1259,1260]
targerIds = [508,509,512,513,514,515,516,517,529,530,531,533,534,536,551,552,553,537,538,539,540,542,543,544,545,546,547,548,549]
## @@ for all id loop @@ ##
# targerIds = []
# with open("./idSets/all_549.csv", 'rb') as fp:
# 	reader = csv.reader(fp ,delimiter=',')
# 	for row in reader:
# 		targerIds.extend(row)

# fileName = datetime.fromtimestamp(t).strftime('%Y-%m-%d_%H:%M:%S')
fileName = 'AV_Samsung.csv'
fw = open('/home/youngcoma/Dropbox/fallDetect/test result/{}'.format(fileName) , 'w')

## @@ Table Header @@ ##
fw.write('TA,SVM,AV,errorRate,FPids,TNids\n')

totalCnt = len(targerIds)
for SVM in np.arange(SVMstart, SVMend, SVMstep):
	for AV in np.arange(AVstart, AVend, AVstep):
		# for TA in np.arange(TAstart, TAend, TAstep):

		## @@ find Max Count @@ ##
		maxCnt = 0
		for _id in targerIds:
			datas = list(database.getTableColsById(cur, 'lab_primitive2', targetCols, _id))
			npDatas = np.array(datas, dtype=zip(targetCols,targetTypes))

			if npDatas[0]['label'] == 1:
				maxCnt = max(maxCnt, len(dataManiplate.findOverThreshold(npDatas, AV, SVM)))

		## @@ Find Treahold @@ ##
		errorCntFP = 0
		errorCntTN = 0
		overMaxCntCnt = 0
		FPbaseIds = []
		TNbaseIds = []

		for _id in targerIds:

			## @@ 400 per base_id data @@ ##
			datas = list(database.getTableColsById(cur, 'lab_primitive2', targetCols, _id))
			npDatas = np.array(datas, dtype=zip(targetCols,targetTypes))
			

			##@@ Cal  TA, SVM, AV @@##
			cnt = len(dataManiplate.findOverThreshold(npDatas, AV, SVM))
			if cnt > 0:
				## @@ non-fall check @@ ##
				if npDatas[0]['label'] == -1:
					errorCntFP+=1
					FPbaseIds.append(npDatas[0]['base_id'])
					
					if cnt > maxCnt:
						overMaxCntCnt+=1
			else:
				## @@ non-fall check @@ ##
				if npDatas[0]['label'] == 1:
					errorCntTN+=1
					TNbaseIds.append(npDatas[0]['base_id'])
			
		## @@  Enable / Disable MaxCount => deduce overMaxCntCnt @@ ##
		errorRate = (errorCntFP+errorCntTN)/ float(totalCnt)
		outputStr = '{},{},{},{},{}\n'.format('0', SVM, AV, errorRate, FPbaseIds, TNbaseIds)
		fw.write(outputStr)


fw.close()
print 'completed'
				## errorRate = (errorCntFP+errorCntTN-overMaxCntCnt)/totalCnt
