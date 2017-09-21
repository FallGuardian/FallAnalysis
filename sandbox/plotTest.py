import matplotlib
import sys
import numpy as np
from shutil import *
import matplotlib.pyplot as plt

from package import *
db = database.initialize()
cur = db.cursor()

targetCols = ['base_id', 'id', 'acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z', 'label']
targetTypes = ['i','i','f','f','f','f','f','f','i']

baseId = sys.argv[1]

datas = list(database.getTableColsById(cur, 'final_primitive_total', targetCols, baseId))
if len(datas) != 400:
	datas = dataManiplate.dataExtend(datas)
npDatas = np.array(datas, dtype=zip(targetCols,targetTypes))

alpha = 0.5
linearAcc = [dataManiplate.highPassFilter(d['acc_x'], d['acc_y'], d['acc_z'], alpha) for d in npDatas]

acc_x = [d['acc_x'] for d in npDatas]
linearAcc_x = [d[0]for d in linearAcc]

# linearAcc_y = [d[1]for d in linearAcc]
# linearAcc_z = [d[2]for d in linearAcc]

plt.plot( range(len(linearAcc_x)), linearAcc_x, 'b',range(len(acc_x)), acc_x, 'c')
# plt.plot( range(len(linearAcc_x)), linearAcc_x, 'r', \
# 	range(len(linearAcc_y)), linearAcc_y, 'b',range(len(linearAcc_z)), linearAcc_z,'g')
plt.axis([0, 400, -25, 25])
plt.show()
# plt.savefig("myfig.png")
# copyfile('myfig.png', '/home/youngcoma/Dropbox/newFallDetect/experiment/myfig_copy.png')