import csv
import sys

from classes.fallDetector import FallDetector
from package import *
db = database.initialize()
cur = db.cursor()

basePath = "/home/youngcoma/Dropbox/newFallDetect/experiment"
fileName = sys.argv[1]
targerIds = []
with open("{}/input_id/{}".format(basePath, fileName), 'rb') as fp:
	reader = csv.reader(fp ,delimiter=',')

	for row in reader:
		 for item in row:
		 	if item:
				targerIds.append(item)

fd = FallDetector(cur, targerIds)
# fd.generateData()
fd.test()

fd = None