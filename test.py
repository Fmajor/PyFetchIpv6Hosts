dict={
	'ie':'utf-8',
	'mod':0,
	'isid':'1B18766355E93136',
	'pstg':0,
	'wd':123,
	'tn':'baidu',
	'ie':'utf-8',
	'rsv_bp':0,
	'rsv_spt':3,
	'rsv_sug3':2,
	'rsv_sug4':58,
	'rsv_sug1':2,
	'inputT':12036,
	'rsv_sid':'7017_1437_5223_6996_7057_4759_6017_7159_6983_7105',
	'f4s':1,
	'csor':0,
	'_cr':115982
	}

proxies = { 
	      "http": "http://127.0.0.1:8888",
}

import requests
get = requests.get
task0 = get('http://www.baidu.com',params=dict,proxies=proxies)

import urllib

params = { 
	"vjsRef":"http://cloudmonitor.ca.com/en/ping.php?vtt=%s&varghost=%s&vhost=_&vaction=ping&ping=Start",
	"vref_string":"%s::http://cloudmonitor.ca.com/en/ping.php?vtt=%s&amp;varghost=%s&amp;vhost=_&amp;vaction=ping&amp;ping=Start::ping.php?vtt=%s8&amp;varghost=%s&amp;vhost=_&amp;vaction=ping&amp;ping=Start",
	"vserverRef":"http://cloudmonitor.ca.com/en/ping.php?vtt=%s&amp;varghost=%s&amp;vhost=_&amp;vaction=ping&amp;ping=Start"}
paramsArray = params.items()
paramsArray.sort()
url = '?'
for eachPair in paramsArray:
	url = url + eachPair[0] + "=" + eachPair[1] + "&"

url = url[:-1]
import sys
import time
def oneLinePrint(printStr):
	sys.stdout.write(printStr+"\r")
	sys.stdout.flush()

oneLinePrint('hehe')
time.sleep(1)
oneLinePrint('hehe haha')
print 

