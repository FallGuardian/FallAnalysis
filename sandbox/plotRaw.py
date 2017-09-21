import sys
from package import *

db = database.initialize()
cur = db.cursor()

targetCols = ['base_id', 'id', 'acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z', 'label']
targetTypes = ['i','i','f','f','f','f','f','f','i']
targetTable = 'final_primitive_total'

##	read target base_id to plot
baseId = sys.argv[1]

if baseId == "all":
	for d in database.getColDistinct(cur, 'final_primitive_total', 'base_id'):
		generalPlot.plotRaw(cur, d, targetCols, targetTypes, targetTable)
		print d
else:
	generalPlot.plotRaw(cur, baseId, targetCols, targetTypes, targetTable)

cur.close()
