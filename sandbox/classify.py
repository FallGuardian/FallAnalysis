import numpy as np
import mlpy
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt 
import matplotlib.cm as cm

rawData = np.loadtxt('data/data.csv', delimiter=',')


fall = [int(row[0]) for row in rawData if row[4] == 1]

fallDatas = np.asarray([row for row in rawData if row[4] == 1])
# otherBehaviorDatas = [row for row in rawData if row[4] == -1]

# data = rawData
data = fallDatas
baseIds, x, y = data[:, 0].astype(np.int),data[:, 1:4], data[:, 4].astype(np.int)
SVMmax, deltaTAmax, SVMSTD = data[:, 1], data[:, 2],data[:, 3]

sitting = [219,368,629,983,984,985,1022,1023,1024,1092,1093,1094,817,818,819,447,448,496,497,218,374,986,1059,1060,1025,1026,1095,1097,933,934,]
lying = [449,217,600,801,375,1061,1062,1027,1098,1099,1163,820,821,823,935,936,937,]

upstair = [354,579,575,547,548,549,736,737,738,809,810,811,584,585,586,1017,1019,1021,1068,1105,1107,1109,1151,1154,1156,1279,1280,1270,1271]
downstair = [353, 576,577,578,573,574,544,545,546,733,734,735,350,351,806,807,808,587,588,589,1016,1018,1020,1066,1067,1069,1032,1033,1034,1106,1108,1110,1152,1155,1157,1276,1277,1278,1272,1273,1274,1265,1267,1269]

jump = [581,434,580,469,470,471,493,494,495,551,552,553,722,723,724,347,601,602,799,800,417,418,419,626,627,628,987,988,989,1088,1089,1090,1035,1036,1037,1111,1112,1113,1148,1149,1150,824,828,829,1261,1262,1263,1258,1259,1260]

walking = [554,537,538,539,718,719,348,221,803,804,592,590,591,631,1028,880,881,882,]
running = [355,555,556,558,559,560,567,569,570,540,542,543,729,730,732,349,352,223,813,814,596,597,632,633,634,1013,1014,1015,1063,1064,1065,1029,1030,1031,1101,1102,1104,1158,1162,1161,884,885,886,890,891,892,893,894,895]

# position
waist = [453,454,458,455,456,457,460,461,462,463,464,465,466,467,468,1070,1072,1073,1075,1076,1077,1079,1080,1081,1082,1083,1084,1085,1086,1087,1225,1227,1228,1222,1223,1224,1235,1236,1240,1232,1231,1233,1248,1249,1250]
thigh =[837,840,841,851,852,853,847,848,849,842,843,845,831,832,836,991,992,995,996,999,1000,1004,1006,1007,994,1001,1002,1008,1009,1010,388,392,393,390,394,425,391,428,429,389,426,427,430,431,432]
Chest =[475,476,477,478,479,480,481,482,485,486,487,488,489,490,491,1039,1042,1043,1046,1044,1047,1051,1052,1053,1048,1049,1050,1054,1056,1057,1202,1203,1204,1205,1211,1212,1213,1206,1207,1209,1216,1218,1219,1200,1201]

# smartphone brand
HTC = [388,392,393,390,394,425,391,428,429,389,426,427,430,431,432,341,777,604,345,781,607,343,780,605,342,778,606,346,782,603]
Samsung = [792,793,794,783,784,785,789,790,791,786,787,788,795,796,797,744,745,747,748,749,750,751,752,753,754,755,757,741,742,743]

yColor = []

for i in baseIds:
	## position set in fallData ##
	# if i in waist:
	# 	yColor.append('#FF9900')
	# elif i in thigh:
	# 	yColor.append('r')
	# elif i in Chest:
	# 	yColor.append('g')
	# else:
	# 	yColor.append('w')

	## smartphone brand
	if i in HTC:
		yColor.append('#FF9900')
	elif i in Samsung:
		yColor.append('g')
	else:
		yColor.append('w')

	## motion set 1 ##
	# if i in sitting:
	# 	yColor.append('b')
	# elif i in lying:
	# 	yColor.append('g')
	# # elif i in fall:
	# # 	yColor.append('r')
	# else:
	# 	yColor.append('w')
	
	## motion set 2 ##
	# if i in upstair:
	# 	yColor.append('b')
	# elif i in downstair:
	# 	yColor.append('g')
	# # elif i in fall:
	# # 	yColor.append('r')
	# else:
	# 	yColor.append('w')

	## motion set 3 ##
	# if i in running:
	# 	yColor.append('b')
	# elif i in walking:
	# 	yColor.append('g')
	# # elif i in fall:
	# # 	yColor.append('r')
	# else:
	# 	yColor.append('w')

	## motion set 4 ##
	# if i in jump:
	# 	yColor.append('b')
	# # elif i in fall:
	# # 	yColor.append('r')
	# else:
	# 	yColor.append('w')



# 3D figure
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(SVMmax, deltaTAmax, 0, c=yColor, marker="o")
# ax.set_xlabel('SVMmax')
# ax.set_ylabel('deltaTAmax')
# ax.set_zlabel('SVMSTD')
# plt.show();

# 2D SVMmax, TAdeltaMax
d = 3
# title = plt.title("blue:sitting, green:lying, \n red:fall, white:other behavior")
# title = plt.title("blue:upstair, green:downstair, \n red:fall, white:other behavior")
# title = plt.title("blue:running, green:walking, \n red:fall, white:other behavior")
# title = plt.title("blue:jump, \n red:fall, white:other behavior")
title = plt.title("orange:waist, red:thigh, \n green:Chest, white:other position")
title = plt.title("orange:HTC, red:Samsung, \n  white:other brand")
plt.set_cmap(plt.cm.Paired)
plot = plt.scatter(deltaTAmax, SVMmax, s=30, c=yColor, alpha=1)
plt.axis([(min(deltaTAmax)-d), (max(deltaTAmax)+d), (min(SVMmax)-d),(max(SVMmax)+d)])
labx = plt.xlabel("deltaTAmax")
laby = plt.ylabel("SVMmax")
plt.show()


# PCA analysis 
# pca = mlpy.PCA()
# pca.learn(x) 
# z = pca.transform(x, k=2)
# plt.set_cmap(plt.cm.Paired)
# fig1 = plt.figure(1)
# title = plt.title("PCA on fall rawDataset")
# plot = plt.scatter(z[:, 0], z[:, 1], c=yColor)
# labx = plt.xlabel("First component")
# laby = plt.ylabel("Second component")
# plt.show()