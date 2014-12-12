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

TAdeltaStart, TAdeltaEnd = 0,175
AVdeltaStart, AVdeltaEnd = 0, 45
TAdeltaStep = 1
## @@ id Setting @@ ##
targerIds = [219,368,629,983,984,985,1022,1023,1024,1092,1093,1094,817,818,819,447,448,496,497,218,374,986,1059,1060,1025,1026,1095,1097,226,449,217,600,801,375,1061,1062,1027,1098,1099,1163,820,821,823,554,537,538,539,718,719,348,221,803,804,592,590,591,631,1028,880,881,882,355,555,556,558,559,560,567,569,570,540,542,543,729,730,732,349,352,223,813,814,596,597,632,633,634,1013,1014,1015,1063,1064,1065,1029,1030,1031,1101,1102,1104,1158,1162,1161,884,885,886,890,891,892,893,894,895,353,576,577,578,573,574,544,545,546,733,734,735,350,351,806,807,808,587,588,589,1016,1018,1020,1066,1067,1069,1032,1033,1034,1106,1108,1110,1152,1155,1157,1276,1277,1278,1272,1273,1274,1265,1267,1269,354,579,575,547,548,549,736,737,738,809,810,811,584,585,586,1017,1019,1021,1068,1105,1107,1109,1151,1154,1156,1279,1280,1270,1271,581,434,580,469,470,471,493,494,495,551,552,553,722,723,724,347,601,602,799,800,417,418,419,626,627,628,987,988,989,1088,1089,1090,1035,1036,1037,1111,1112,1113,1148,1149,1150,824,828,829,1261,1262,1263,1258,1259,1260,388,392,393,453,454,458,475,476,477,508,509,744,745,747,341,777,604,792,793,794,398,397,396,608,612,991,992,995,1070,1072,1073,1039,1042,1043,1114,1115,1116,1142,1143,1144,837,840,841,1200,1201,1202,1225,1227,1228,390,394,425,455,456,457,478,479,480,512,513,514,748,749,750,345,781,607,783,784,785,399,400,598,615,619,996,999,1000,1075,1076,1077,1046,1044,1047,1117,1118,1119,1139,1140,1141,851,852,853,1203,1204,1205,1222,1223,1224,391,428,429,460,461,462,481,482,485,515,516,517,751,752,753,343,780,605,789,790,791,404,405,406,610,614,618,1004,1006,1007,1079,1080,1081,1051,1052,1053,1120,1121,1123,1133,1134,1135,847,848,849,1211,1212,1213,1235,1236,1240,389,426,427,463,464,465,486,487,488,529,530,531,754,755,757,342,778,606,786,787,788,408,409,609,613,617,994,1001,1002,1082,1083,1084,1048,1049,1050,1125,1126,1127,1136,1137,1138,842,843,845,1206,1207,1209,1232,1231,1233,430,431,432,466,467,468,489,490,491,533,534,536,741,742,743,346,782,603,795,796,797,599,413,416,620,622,624,1008,1009,1010,1085,1086,1087,1054,1056,1057,1129,1131,1132,1145,1146,1147,831,832,836,1216,1218,1219,1248,1249,1250]

## @@ for all id loop @@ ##
# targerIds = []
# with open("./idSets/all_549.csv", 'rb') as fp:
# 	reader = csv.reader(fp ,delimiter=',')
# 	for row in reader:
# 		targerIds.extend(row)

## @@ getDelta Data @@ ##
data = np.loadtxt('./data/data_all_549.csv', delimiter=',')
# x, y = data[:, 0:4], data[:, 4].astype(np.int)
base_id, attrs = data[:, 0].astype(np.int), data[:,2:5] 


deltaData = dict(zip(base_id,attrs))

fileName = 'TAdelta+SVM.csv'
fw = open('/home/youngcoma/Dropbox/fallDetect/test result/{}'.format(fileName) , 'w')

## @@ Table Header @@ ##
fw.write('SVM,TAdelta,errorRate,FPids,TNids\n')

totalCnt = len(targerIds)
for SVM in np.arange(SVMstart, SVMend, SVMstep):
	for TAdelta in np.arange(TAdeltaStart, TAdeltaEnd, TAdeltaStep):

		## @@ find Max Count @@ ##
		# maxCnt = 0
		# for _id in targerIds:
		# 	datas = list(database.getTableColsById(cur, 'lab_primitive2', targetCols, _id))
		# 	npDatas = np.array(datas, dtype=zip(targetCols,targetTypes))

		# 	if npDatas[0]['label'] == 1:
		# 		max(maxCnt, len(dataManiplate.findOverThreshold(npDatas, AV, SVM)))

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
			

			##@@ Cal SVM, TAdelta @@##
			if deltaData[_id][0] > TAdelta and len(dataManiplate.findOverSVM(npDatas, SVM)) > 0:

					## @@ non-fall check @@ ##
					if npDatas[0]['label'] == -1:
						errorCntFP+=1
						FPbaseIds.append(npDatas[0]['base_id'])
						
						# if cnt > maxCnt:
						# 	overMaxCntCnt+=1
			else:
				## @@ non-fall check @@ ##
				if npDatas[0]['label'] == 1:
					errorCntTN+=1
					TNbaseIds.append(npDatas[0]['base_id'])
			
		## @@  Enable / Disable MaxCount => deduce overMaxCntCnt @@ ##
		errorRate = (errorCntFP+errorCntTN-overMaxCntCnt)/ float(totalCnt)
		outputStr = '{},{},{},{}\n'.format(SVM, TAdelta, errorRate, FPbaseIds, TNbaseIds)
		fw.write(outputStr)


fw.close()
print 'completed'
				## errorRate = (errorCntFP+errorCntTN-overMaxCntCnt)/totalCnt
