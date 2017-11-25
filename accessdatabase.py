from http.server import BaseHTTPRequestHandler, HTTPServer
import sqlite3
import time
class MyHandler(BaseHTTPRequestHandler):
 
    # HTTP REQUESTS HERE
    pass

def saveData(id, data):
	conn = sqlite3.connect('databasename.db')
	c = conn.cursor()
	for sensor, value in data.items():
		c.execute("INSERT INTO data VALUES('"+id+"', '"+sensor+"',"+ str(value)+", "+str(time.time())+")")
	conn.commit()
	print("Saved")


def getData(id, sensor, start, end):
	conn = sqlite3.connect('databasename.db')
	c = conn.cursor()
	if(end==-1):
		end=time.time()
	if(start == -1):
		start = 0
	if(id == - 1 and sensor == -1):
		value = c.execute("SELECT * FROM data WHERE timeIn < end2=:endtime and timeIn > start2=:starttime ", {"endtime":end,"starttime":start})
	elif(id == -1):
		value = c.execute("SELECT * FROM data WHERE sensor=:sensor and timeIn < end2=:endtime and timeIn > start2=:starttime ", {"sensor": sensor, "endtime":end,"starttime":start})
	elif(sensor == -1):
		value = c.execute("SELECT * FROM data WHERE id=:who and timeIn <:endtime and timeIn >:starttime ", {"who": id, "endtime":end,"starttime":start})
	else:
		value = c.execute("SELECT * FROM data WHERE id=:who and sensor=:sensor and timeIn <:endtime and timeIn >:starttime ", {"who": id, "sensor": sensor, "endtime":end,"starttime":start})
	values = []
	for r in value:
		values.append(r[2])
	return values
 
 
def run():
	conn = sqlite3.connect('databasename.db')
	c = conn.cursor()
	try:
		c.execute('''CREATE TABLE data (id text, sensor text, value real, timeIn real)''')
		c.commit()
	except Exception as e:
		print(e)
	conn.close()
	#saveData('id2',{"air":5, "light":3})
	#saveData('id1',{"air":7, "light":5})
	print(getData("id2","air", -1,-1)) #gives all time value of mbed 2 air quality
	print(getData("id2","air", time.time()-24*3600,-1))  #gives value of mbed 2 air quality in the preceding 24 h
	print(getData("id1",-1, -1,-1)) #gives all time all sensors value of mbed 1
if __name__ == '__main__':
    run()