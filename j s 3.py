from http.server import *
import socketserver
import socket
import time
import json
import sqlite3


JD = json.JSONDecoder()
JE = json.JSONEncoder()
events = dict()

mbeds = list()
mbed_eids = dict() ##mbed event ids
mbed_queues = dict() ##mbed events to be queued


def clear_queue(mbed_id):
    tuple_list = mbed_queues[mbed_id]
    string = "{"
    for name, val in tuple_list:
        string += '"'+str(name)+'":'+str(val)+','
    string = string[:-1]
    string += '}'
    mbed_queues[mbed_id] = list()
    return string


def add_event_to_queue(mbed_id, conditions, event_id):
    event = [("create", event_id),] + conditions + [("end", 1)]
    mbed_queues[mbed_id].extend(event)


def bind_event(mbed_id, conditions, action):
    event = {'mbed_id' : mbed_id,
             'conditions' : conditions,
             'action' : action}
    eid = id(event)
    events[eid] = event
    
    mbed_eids[mbedid].append(eid)
    add_event_to_queue(mbedid, conditions, eid)

def event_response(event_id):
    action = events[event_id]['action']
    del events[event_id]
    action()

def post_from_mbed(data):
    data = JD.decode(data);
    if 'event' in data:
        event_response(data['event']) 
    elif 'mbed_id' in data:
        print(data)

def get_from_mbed(data):
    data = JD.decode(data);
    if 'query' in data:
        clear_queue()
        print()


def add_mbed(id):
    mbed_queues[id] = list()
    mbed_eids[id] = list()


mbedid = "d4:ca:6e:77:df:2a"
add_mbed(mbedid)
def test_func():
    print("Hello World!")

bind_event(mbedid, [("xacc_s", 0),], test_func)


        

    

##def rebind_e(mbed_id, event):
##    _, conditions, eid = event
##    try:
##        msend(mbedid, conditions, eid)
##    except Exception as E:
##        print(E)
##        pass

##def mbed_reload(mbed_id):
##    for eid in mbeds_eids:
##        event = events[eid]
##        rebind_e(mbedid, event)






        

def saveData(id, data):
    conn = sqlite3.connect('databasename.db')
    c = conn.cursor()
    for sensor, value in data.items():
        c.execute("INSERT INTO data VALUES('"+id+"', '"+sensor+"',"+ str(value)+", "+str(time.time())+")")
    conn.commit()
    print("Saved")
def saveEvent(id, sensor, thresh, action):
    conn = sqlite3.connect('databasename.db')
    c = conn.cursor()
    for sensor, value in data.items():
        c.execute("INSERT INTO data VALUES('"+id+"', '"+sensor+"',"+ str(tresh)+", '"+action+"'')")
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

    #saveData('id2',{"air":5, "light":3})
    #saveData('id1',{"air":7, "light":5})
    print(getData("id2","air", -1,-1)) #gives all time value of mbed 2 air quality
    print(getData("id2","air", time.time()-24*3600,-1))  #gives value of mbed 2 air quality in the preceding 24 h
    print(getData("id1",-1, -1,-1)) #gives all time all sensors value of mbed 1

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        length = int(self.headers["content-length"])
        try:
            if self.path == "/":
                self.send_file("index.html", "text/html")
            elif self.path == "/mbed":
                data = self.rfile.read(length).decode("utf-8")
                #print(str(data))
                mbed_id = JD.decode(str(data))["query"]
                s = clear_queue(mbed_id)
                #print(type(s))
                self.wfile.write(s.encode('utf-8'))
            else:
                self.send_file(self.path[1:])
        except Exception as e:
            print(e)

    def do_POST(self):
        self.send_response(200)
        length = int(self.headers["content-length"])
        data = self.rfile.read(length)
        if self.path == "/mbed":
            post_from_mbed(data)
        else:
            print(data)
            json_data = json.loads(data)
            saveEvent(json_data['mbetnumber'],json_data['sensornumber'],json_data['tresh'],json_data['actionnumber'])
            self.send_file("index.html", "text/html")

    def send_file(self, filename, encoding=None):
        with open(filename, "rb") as file:
            self.send_response(200)
            if not encoding:
                self.send_header("Content-type", encoding)
            self.end_headers()
            self.wfile.write(file.read())

if __name__ == "__main__":
    conn = sqlite3.connect('databasename.db')
    c = conn.cursor()
    try:
        c.execute('''CREATE TABLE data (id text, sensor text, value real, timeIn real)''')
        c.commit()
    except Exception as e:
        print(e)
    conn.close()
    conn2 = sqlite3.connect('events.db')
    c2 = conn2.cursor()
    try:
        c2.execute('''CREATE TABLE data (id text, sensor text, value real, action text)''')
        c2.commit()
    except Exception as e:
        print(e)
    conn2.close()
    with socketserver.TCPServer(("", 8080), Handler) as httpd:
        print("HTTP server running on port 8080")
        print("Your IP address is: ", socket.gethostbyname(socket.gethostname()))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(" Recieved Shutting Down")




