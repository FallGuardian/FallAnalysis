import os

basePath = "/home/youngcoma/Dropbox/newFallDetect/experiment/input_id"
srciptPath = "/home/youngcoma/workplace/analysis_py/sandbox/algSVMmaxmin.py"
for dirname, dirnames, filenames in os.walk(basePath):
	for name in filenames:
		print name

os.popen(srciptPath)