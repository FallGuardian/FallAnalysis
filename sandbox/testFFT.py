import matplotlib.pyplot as plt
import numpy as np
import database
import sys
import dataManiplate

db = database.initialize()
cur = db.cursor()

_id = sys.argv[1]

targetCols = ['base_id', 'id', 'acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z', 'label']
targetTypes = ['i','i','f','f','f','f','f','f','i']
datas = list(database.getTableColsById(cur, 'final_primitive_total', targetCols, _id))

if len(datas) == 400:
	print '{} is broken'.format(_id)
	last = len(datas) - 1
	print last
	appendData = map(tuple, ( (0,0,datas[last][2],
			datas[last][3],
			datas[last][4],
			datas[last][5],
			datas[last][6],
			datas[last][7],0)for i in range(len(datas), 400)))
	print appendData
	datas = datas + appendData

npDatas = np.array(datas, dtype=zip(targetCols,targetTypes))

SVMColumn = [dataManiplate.calSVM(d['acc_x'], d['acc_y'], d['acc_z']) for d in npDatas]
TAColumn = [dataManiplate.calTA(d['acc_x'], d['acc_y'], d['acc_z']) for d in npDatas]

t = np.arange(400)
sp = np.fft.fft(SVMColumn)
freq = np.fft.fftfreq(t.shape[-1])
# plt.plot(freq, sp.real, freq, sp.imag)
plt.plot(freq, sp.real, 'r')
plt.plot(freq, sp.imag, 'b')
plt.show()