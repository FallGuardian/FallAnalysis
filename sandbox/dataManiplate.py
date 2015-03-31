import math
import numpy as np

def calVelocity( acc_x, acc_y, acc_z ):
	return (math.sqrt(math.pow(acc_x,2)+math.pow(acc_y,2)+math.pow(acc_z,2))-9.81)

# Questino: Do I need to model the function of angular displacement ?
def calAngularDisplacement( gyroCumulation, sample_timing ):
	return gyroCumulation*sample_timing

def calGyroCumulation( gyroArr ):
	gyroCumulation = 0
	for constant,index in zip(range(400,0,-1),range(0,400)):
		# print "i={}, j={}".format(constant,index)
		gyroCumulation += gyroArr[index][0]*constant

	return gyroCumulation
def calVecolity():
	return
def calSVM( acc_x, acc_y, acc_z ):
	return math.sqrt(math.pow(acc_x,2)+math.pow(acc_y,2)+math.pow(acc_z,2))

def calTA( acc_x, acc_y, acc_z ):
	if acc_x != 0 and acc_y != 0 and acc_z != 0:
		return math.asin(acc_y/(math.sqrt(math.pow(acc_x,2)+math.pow(acc_y,2)+math.pow(acc_z,2))))*180/math.pi
	else:
		return 0

def calAV( acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z ):
	return abs(acc_x*math.sin(gyro_x)+acc_y*math.sin(gyro_y)-acc_z*math.cos(acc_y)*math.cos(acc_z))

def findOverThreshold(npDatas, AV, SVM):
	overIds = []
	for d in npDatas:
		if calSVM(d['acc_x'], d['acc_y'], d['acc_z']) > SVM and calAV(d['acc_x'], d['acc_y'], d['acc_z'], d['gyro_x'], d['gyro_z'], d['acc_z']) > AV:
			overIds.append(d['id'])

	return overIds

def findOverThreshold2(npDatas, TA, SVM):
	overIds = []
	for d in npDatas:
		if calTA(d['acc_x'], d['acc_y'], d['acc_z']) > TA and calSVM(d['acc_x'], d['acc_y'], d['acc_z']) > SVM:
			overIds.append(d['id'])

	return overIds

def findOverSVM(npDatas, SVM):
	overIds = []
	for d in npDatas:
		if calSVM(d['acc_x'], d['acc_y'], d['acc_z']) > SVM:
			overIds.append(d['id'])

	return overIds
