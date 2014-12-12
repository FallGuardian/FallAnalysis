#encoding=UTF-8
import sys
import MySQLdb

# Database intilization & prompt
def initialize():
	# 
	_host = "localhost"
	_user = "fallDetect"
	_pswd = "EtXpphf2bQ78QGBJ"
	_db = "fallDetect"
	#
	db = MySQLdb.connect(host=_host, user=_user, passwd=_pswd, db=_db)
	if db is None:
		print 'Fail to connect'
	else:
		print 'Connect infomation => host: '+_host+', database: '+_db
	return db.cursor()

def getFormatedData(cur, baseId):
	cur.execute("SELECT * FROM `formated_data` WHERE `base_id`=%(baseId)s",{'baseId':baseId})
	return cur.fetchall()

def getTempFormatedData(cur, baseId):
	cur.execute("SELECT * FROM `formated_data2` WHERE `base_id`=%(baseId)s",{'baseId':baseId})
	return cur.fetchall()



def getSMAs(cur, ids):
	data = []	
	for i in ids:
		if type(i) is int:
			data.append(0)
		elif type(i) is tuple:
			cur.execute("SELECT `SMA` FROM `lab_primitive` WHERE `id`=%(id)s", {'id':(i[0]*400+1)} )
			SMA = cur.fetchone()
			if SMA is None:
				data.append(0)
			else:
				data.append(SMA[0])

	return data

def getBaseId(cur):
	cur.execute("SELECT * FROM `id_base`")
	return list(cur.fetchall())

def getBaseIdByFormated(cur):
	cur.execute("SELECT DISTINCT `base_id` FROM `formated_data`")
	return cur.fetchall()

def getFallId(cur):
	cur.execute("SELECT * FROM `fall_id`")
	return list(cur.fetchall())

def serializeId(target, all):
	rst = []
	for baseId in all:
		if baseId in target:
			rst.append(baseId)
		else:
			rst.append(0)

	return rst

def overThreadHold(cur, id_base):
	start = id_base*400
	end = id_base*400+400
	cur.execute("SELECT `id` FROM `lab_primitive` WHERE `id`>%s AND `id`<=%s", (start, end))
	return cur.fetchall()

# Generenic Function For Database
def getTableColsById(cur, tableName, colNames, idValue):
	ss = ','.join(['`{}`'.format(s) for s in colNames])
	sql = 'SELECT '+ss+' FROM `{}` WHERE `base_id`=%(idValue)s ORDER BY `id`'.format(tableName)
	cur.execute(sql,{'idValue':idValue})
	return cur.fetchall()

def getTableAll(cur, tableName):
	sql="SELECT * FROM `{}`".format(tableName)
	cur.execute(sql)
	return cur.fetchall()

def getCol(cur, tableName, colName):
	sql = "SELECT `{}` FROM `{}`".format(colName,tableName)
	cur.execute(sql)
	return cur.fetchall()

def getColDistinct(cur, tableName, colName):
	sql = "SELECT DISTINCT `{}` FROM `{}`".format(colName,tableName)
	cur.execute(sql)
	return cur.fetchall()

def getTableRowsByColValue(cur, tableName, colName, colValue):
	sql = "SELECT * FROM `{}` WHERE `{}`=%(colValue)s".format(tableName, colName)
	cur.execute(sql,{'colValue':colValue})
	return cur.fetchall()


