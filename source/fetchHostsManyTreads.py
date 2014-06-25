# -*- coding: utf-8 -*-
#
#         (__)              PyFetchIpv6Hosts
#         (oo)
#   /------\/               Distributed under
#  / |    ||             the GNU GPL v3 License
# *  /\---/\
#    ~~   ~~               http://www.gnu.org
#
#
# 2014-06-22
#
# Author: wujinnnnn@gmail.com

from bs4 import BeautifulSoup
import re,requests,json,os,pickle,time,sys,commands
import pdb 
import threading

#proxies = {
#	  "http": "http://127.0.0.1:8888",
#}


def oneLinePrint(printStr):
	sys.stdout.write(printStr+"\r")
	sys.stdout.flush()

def view_bar(num=0, sum=10, bar_word="="):   
	bar = bar_word * num
	sys.stdout.write('\t'+str(int(num*100.0/sum))+'%  ['+bar+' '*(sum-num)+"]\r")
	sys.stdout.flush()

def ping(urlStr):
	pingCommand = 'ping -c 2 ' + urlStr;
	print pingCommand
	(status, output) = commands.getstatusoutput(pingCommand)
	if status>0:
		return -1
	else:
		timeList = re.findall(r"time=(.*) ms",output)
		meantime = 0
		for eachTime in timeList:
			meantime += float(eachTime)
		meantime = meantime/2
		return meantime

def ping6(urlStr,printStr=''):
	pingCommand = '\tping6 -c 2 ' + urlStr 
	(status, output) = commands.getstatusoutput(pingCommand)
	if status>0:
		print pingCommand + printStr + '\tping not successful!!!!!!!!!!!!'
		return -1
	else:
		timeList = re.findall(r"time=(.*) ms",output)
		meantime = 0
		for eachTime in timeList:
			meantime += float(eachTime)
		meantime = meantime/2
		print pingCommand, '\tmeantime:',meantime,'\t',printStr
		return meantime

def getIP():
	root = 'http://20140507.ip138.com/ic.asp'
	headers = {
	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.56 Safari/537.17',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'en-US,en;q=0.8'}
	s = requests.Session()
	s.headers = headers
	#s.proxies=proxies
	html = s.get(root).text
	soup = BeautifulSoup(html)
	ip = re.findall(r"\[(.*)\]",soup.text)[0]
	return ip


class justPing():
	def __init__(self):
		self.localip = getIP()
		self.headers = {
		'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.56 Safari/537.17',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Encoding': 'gzip,deflate,sdch',
		'Accept-Language': 'en-US,en;q=0.8'}
		self.root = 'http://cloudmonitor.ca.com'
		self.s = requests.Session()
		self.s.headers = self.headers
		#self.s.proxies=proxies
		if not os.path.exists('data/eachURLdata'):
			os.mkdir('data/eachURLdata')

	def getIpv6Address(self, urlStr):
		print "just-ping ", urlStr
		statusStr = '\t'
		# get vtt in the page
		html = self.s.get(self.root+'/en/ping.php').text
		soup = BeautifulSoup(html)
		vtt = soup.findAll('input', {'name':'vtt','value':re.compile('.*')})[0].attrs['value']
		#statusStr = statusStr+'get vtt.....'; oneLinePrint(statusStr)
		# get uid in the page
		temStr = "/en/ping.php" 
		params = {
			'vtt':vtt,
			'varghost':urlStr,
			'vhost':'_',
			'vaction':'ping',
			'ping':'Start'}
		html = self.s.get(self.root + temStr,params=params).text
		uid = re.findall(r"uid=(.*)'",html)[0]
		#statusStr = statusStr+'get uid.....'
		oneLinePrint(statusStr)
		t = re.findall(r",\ t:\ (.*)\ }",html)[0]
		#statusStr = statusStr+'get T.....'; oneLinePrint(statusStr)
		# checkreferrer
		#statusStr = statusStr+'checkRef.....'; oneLinePrint(statusStr)
		temStr = '/en/api/checkreferrer.php'
		params = { 
		"vjsRef":"http://cloudmonitor.ca.com/en/ping.php",
		"vref_string":"%s::http://cloudmonitor.ca.com/en/ping.php?vtt=%s&amp;varghost=%s&amp;vhost=_&amp;vaction=ping&amp;ping=Start" 
		% (self.localip,vtt,urlStr),
		"vserverRef":"http://cloudmonitor.ca.com/en/ping.php"}
		req = self.s.get(self.root + temStr,params=params)
		# get data in the page
		temStr = "/en/api/pingproxy.php"
		params = {
			"uid":uid}
		postData = {
			'host':urlStr,
			't':t}
		req = self.s.post(self.root + temStr,params=params,data=postData)
		params = {
			"uid":uid,
			"host":urlStr,
			"v":0}
		resultArray = []
		#statusStr = statusStr+'get data'; oneLinePrint(statusStr)
		for i in range(1,10):
			#view_bar(i,10)
			#print i/10.0*100,'%'
			params["v"] = i
			try:
				resultArray.append(self.s.get(self.root + temStr,params=params,timeout=9).json())
			except:
				break
			time.sleep(0.1)
		temp = {}
		for i in range(len(resultArray)):
			temp.update(resultArray[i]['r'])
		temp = temp.values()
		temp = [each['result'] for each in temp if each.has_key('result')]
		temp = [each['ip'] for each in temp]
		temp = [each for each in temp if each.find(':')>0]
		n = len(temp)
		if n>0:
			print urlStr," get ",n," ipv6 address"
			with open('data/eachURLdata/'+urlStr+'.dat','w') as f:
				tempDict = {urlStr:temp}
				pickle.dump(tempDict,f)
			return temp
		else:
			print urlStr, 'no ipv6 address'
			return []
	
def div_list(ls,n):
	if not isinstance(ls,list) or not isinstance(n,int):
		return []
	ls_len = len(ls)
	if n<=0 or 0==ls_len:
		return []
	if n > ls_len:
		return []
	elif n == ls_len:
		return [[i] for i in ls]
	else:
		j = ls_len/n
		k = ls_len%n
		ls_return = []
		for i in xrange(0,n*j,j):
			ls_return.append(ls[i:i+j])
		for i in xrange(k):
			ls_return[i].append(ls[n*j+i])

		return ls_return

def getHostsViaJustPing(tNumbers,updateAll=0):
	global eachN
	if not os.path.exists('data'):
		os.mkdir('data')

	finishedURL = os.listdir('data/eachURLdata')
	finishedURL = [each[:-4] for each in finishedURL]

	urlFile = open(urlFilePath,'r')
	urlList = [eachLine.split('#')[0].rstrip().split('/')[0] for eachLine in urlFile if len(eachLine.split('#')[0].rstrip())>0]
	if not updateAll:
		urlTodo = [var for var in urlList if var not in finishedURL]
	else:
		urlTodo = urlList
	
	totalN = len(urlTodo)
	if totalN<tNumbers:
		raise ValueError,"to much threads.......more than task"
	print totalN, "URLs to get....."
	if totalN==0:
		print 'NO URL to GET!   exit'
		return
	print tNumbers, "threads to do"
	allURLlist = div_list(urlTodo,tNumbers)
	eachN = len(allURLlist[-1])
	print 'each length is ',eachN

	allURLcache = []
	allMutex = []
	allFinishFlag = []
	allFinished = []
	allPingCount = []
	for i in range(tNumbers):
		allURLcache.append([[],[]])
		allMutex.append(threading.Lock())
		allFinishFlag.append([False])
		allFinished.append([[],[]])
		allPingCount.append([0])
	allGetipTreads = []
	for i in range(tNumbers):
		allGetipTreads.append(threading.Thread(target=getIpv6Address,
		                     args=(allURLlist[i],allURLcache[i],allMutex[i],allFinishFlag[i],i+1)))

	for t in allGetipTreads:
		time.sleep(1)
		t.start()
	
	for t in allGetipTreads:
		t.join()


def ping6FromFile(tNumbers, updateAll=0):
	global eachN
	if not os.path.exists('data'):
		os.mkdir('data')

	if os.path.exists(cacheFileName) and os.path.getsize(cacheFileName)>0:
		f = open(cacheFileName,'r')
		finished = pickle.load(f)
		f.close()
		finishedURL = [finished[0][i] for i in range(len(finished[0])) if len(finished[1][i])>0]
		#finishedURL = [finished[0][i] for i in range(len(finished[0]))]
		print 'load %d finished URL from ' % (len(finishedURL)) +  cacheFileName
	else:
		finished = [[],[]]
		finishedURL = []

	urlFile = open(urlFilePath,'r')
	urlList = [eachLine.split('#')[0].rstrip().split('/')[0] for eachLine in urlFile if len(eachLine.split('#')[0].rstrip())>0]
	if not updateAll:
		urlTodo = [var for var in urlList if var not in finishedURL]
	else:
		urlTodo = urlList
	totalN = len(urlTodo)
	pdb.set_trace()
	if totalN<tNumbers:
		raise ValueError,"to much threads.......more than task"
	print totalN, "URLs to get....."
	if totalN==0:
		print 'NO URL to GET!   exit'
		return
	print tNumbers, "threads to do"
	allURLlist = div_list(urlTodo,tNumbers)
	eachN = len(allURLlist[-1])
	print 'each length is ',eachN
	subTnum = 10;

	allURLcache = []
	allMutex = []
	allFinishFlag = []
	allFinished = []
	allPingCount = []
	for i in range(tNumbers):
		allURLcache.append([[],[]])
		allMutex.append(threading.Lock())
		allFinishFlag.append([False])
		allFinished.append([[],[]])
		allPingCount.append([0])
	

	allGetipTreads = []
	allPing6Treads = []
	for i in range(tNumbers):
		allGetipTreads.append(threading.Thread(target=getIpv6AddressFromFile,
		                     args=(allURLlist[i],allURLcache[i],allMutex[i],allFinishFlag[i],i+1)))
		for j in range(subTnum):
			allPing6Treads.append(threading.Thread(target=usePing6,
		    	                 args=(allURLcache[i],allMutex[i],allFinishFlag[i],allFinished[i],i+1,allPingCount[i])))

	for t in allGetipTreads:
		t.start()
	for t in allPing6Treads:
		time.sleep(0.1)
		t.start()
	for t in allPing6Treads:
		t.join()
	
	for eachFinishedList in allFinished:
		finished[0].extend(eachFinishedList[0])
		finished[1].extend(eachFinishedList[1])

	with open(cacheFileName,'w') as f:
		pickle.dump(finished,f)
	
	noIpUrl = [finished[0][i] for i in range(len(finished[0])) if len(finished[1][i])==0]
	notIncUrl = [eachUrl for eachUrl in urlList if eachUrl not in finished[0] ]

	stillTodoUrl = noIpUrl
	stillTodoUrl.extend(notIncUrl)

	with open(urlFilePath+'.stilltodo','w') as f:
		for eachUrl in stillTodoUrl:
			f.write(eachUrl+'\n')


def getHostsViaJustPingAndping6It(tNumbers):
	global eachN
	if not os.path.exists('data'):
		os.mkdir('data')

	if os.path.exists(cacheFileName) and os.path.getsize(cacheFileName)>0:
		f = open(cacheFileName,'r')
		finished = pickle.load(f)
		f.close()
		finishedURL = [finished[0][i] for i in range(len(finished[0])) if len(finished[1][i])>0]
		#finishedURL = [finished[0][i] for i in range(len(finished[0]))]
		print 'load %d finished URL from ' % (len(finishedURL)) +  cacheFileName
	else:
		finished = [[],[]]
		finishedURL = []

	urlFile = open(urlFilePath,'r')
	urlList = [eachLine.split('#')[0].rstrip().split('/')[0] for eachLine in urlFile if len(eachLine.split('#')[0].rstrip())>0]
	urlTodo = [var for var in urlList if var not in finishedURL]
	totalN = len(urlTodo)
	if totalN<tNumbers:
		raise ValueError,"to much threads.......more than task"
	print totalN, "URLs to get....."
	if totalN==0:
		print 'NO URL to GET!   exit'
		return
	print tNumbers, "threads to do"
	allURLlist = div_list(urlTodo,tNumbers)
	eachN = len(allURLlist[0])
	print 'each length is ',eachN
	subTnum = 10;

	allURLcache = []
	allMutex = []
	allFinishFlag = []
	allFinished = []
	allPingCount = []
	for i in range(tNumbers):
		allURLcache.append([[],[]])
		allMutex.append(threading.Lock())
		allFinishFlag.append([False])
		allFinished.append([[],[]])
		allPingCount.append([0])
	

	allGetipTreads = []
	allPing6Treads = []
	for i in range(tNumbers):
		allGetipTreads.append(threading.Thread(target=getIpv6Address,
		                     args=(allURLlist[i],allURLcache[i],allMutex[i],allFinishFlag[i],i+1)))
		for j in range(subTnum):
			allPing6Treads.append(threading.Thread(target=usePing6,
		    	                 args=(allURLcache[i],allMutex[i],allFinishFlag[i],allFinished[i],i+1,allPingCount[i])))

	for t in allGetipTreads:
		time.sleep(1)
		t.start()
	for t in allPing6Treads:
		time.sleep(0.1)
		t.start()
	for t in allPing6Treads:
		t.join()
	
	for eachFinishedList in allFinished:
		finished[0].extend(eachFinishedList[0])
		finished[1].extend(eachFinishedList[1])

	with open(cacheFileName,'w') as f:
		pickle.dump(finished,f)
	
	noIpUrl = [finished[0][i] for i in range(len(finished[0])) if len(finished[1][i])==0]
	notIncUrl = [eachUrl for eachUrl in urlList if eachUrl not in finished[0] ]

	stillTodoUrl = noIpUrl
	stillTodoUrl.extend(notIncUrl)

	with open(urlFilePath+'.stilltodo','w') as f:
		for eachUrl in stillTodoUrl:
			f.write(eachUrl+'\n')

	if anyError:
		print "have ERROR!"

def getIpv6AddressFromFile(urlTodo, URLcache, mutex, finishFlag,tNum):
	getV6N = 0
	eachUrlDataPath = 'data/eachURLdata/'
	for eachUrl in urlTodo:
		eachFileName = eachUrlDataPath+eachUrl+'.dat'
		if os.path.exists(eachFileName):
			with open(eachFileName,'r') as f:
				eachIPgot = pickle.load(f)[eachUrl]

			mutex.acquire()
			URLcache[0].insert(0,eachUrl)
			URLcache[1].insert(0,eachIPgot)
			mutex.release()
			getV6N += 1
		else:
			mutex.acquire()
			URLcache[0].insert(0,eachUrl)
			URLcache[1].insert(0,[])
			mutex.release()
			getV6N += 1
		
		print '\t'*4,'getV6',getV6N,'/',eachN,' in tread ',tNum
	finishFlag[0] = True

def getIpv6Address(urlTodo, URLcache, mutex, finishFlag,tNum):
	brower = justPing()
	getV6N = 0
	try:
		for eachUrl in urlTodo:
			eachIPgot = brower.getIpv6Address(eachUrl)
			mutex.acquire()
			if len(eachIPgot)>0:
				URLcache[0].insert(0,eachUrl)
				URLcache[1].insert(0,eachIPgot)
			else:
				URLcache[0].insert(0,eachUrl)
				URLcache[1].insert(0,[])
			mutex.release()
			getV6N += 1
			print '\t'*4,'getV6',getV6N,'/',eachN,' in tread ',tNum
	except:
		anyError = 1
		print "getV6N connect error" + "!!"*100 + "in tread %d" % (tNum)
	
	finishFlag[0] = True


def usePing6(URLcache, mutex, finishFlag, finished, tNum, pingCount):
	while(not finishFlag[0] or (finishFlag[0] and len(URLcache[0])!=0)):
		time.sleep(1)
		mutex.acquire()
		if len(URLcache[0])>0:
			eachUrl = URLcache[0].pop()
			temp = URLcache[1].pop()
			ping6N = pingCount[0]
			ping6N += 1
			pingCount[0] = ping6N
			mutex.release()
		else:
			mutex.release()
			continue

		if len(temp)==0:
			finished[0].append(eachUrl)
			finished[1].append('')
			print '\t'*4, eachUrl,'added, no ip address.......', ping6N, '/', eachN, '   in tread ', tNum
			continue

		pingTimes = [ping6(eachIP,printStr=' for %s' % (eachUrl)) for eachIP in temp]

		if max(pingTimes)>0:
			pingTimes = [int(each<0)*99999 + each for each in pingTimes]
			index = pingTimes.index(min(pingTimes))
			eachIPgot = temp[index]
			print '\t'*4, eachUrl,'added','\t',ping6N,'/',eachN,'   in tread ',tNum
		else:
			eachIPgot = ''
			print '\t'*4, eachUrl,'added NULL','\t',ping6N,'/',eachN,'   in tread ',tNum

		mutex.acquire()
		finished[0].append(eachUrl)
		finished[1].append(eachIPgot)
		mutex.release()

import getopt

CONFIG = { 
	'urlFiles':'url.txt',
	'tNum':1,
	'mod':1
}   
OPT_CONFIG_MAP = { 
	'-f':'urlFiles',
	'-n':'tNum',
	'-m':'mod'}

def show_usage(fail=True):
	stream = sys.stderr if fail else sys.stdout
	msglist = ["Usage: hehehe",
	"Options:",
	"  -f urlFile\turlFile to use",
	"  -n tNum\tthe number of treads",
	"  -m mod\t 0~4",
	"        \t 0:just-ping and ping6",
	"        \t 1:just-ping",
	"        \t 2:just-ping, update All",
	"        \t 3:ping6",
	"        \t 4:ping6, update All",
	"  -h help\tshow help message"]
	print >> stream, "\n".join(msglist)
	if fail:
		sys.exit(2)
		return None


optspec=""
optspec += "".join([("%s:" % key.strip("-")) for key in OPT_CONFIG_MAP])

try:
	oplist, args = getopt.gnu_getopt(sys.argv[1:], optspec)
except getopt.GetoptError as go_e:
	show_usage()
opdict = dict(oplist)
CONFIG.update(opdict)

if len(oplist)==0:
	show_usage(fail=False)
	sys.exit(0)
elif "-h" in opdict:  # Exit as early as possible if "-h" is in options.
	show_usage(fail=False)
	sys.exit(0)



tNum = int(CONFIG['-n'])
urlFileName = CONFIG['-f']
urlFilePath = 'urlFiles/' + urlFileName
print 'urlFileName is ',urlFileName
											     
cacheFileName = 'data/'+urlFileName+'.cache.dat'
anyError = 0

mode = CONFIG['-m']
if mode=='0':
	print 'getHostsViaJustPingAndping6It(%s)' % tNum
	time.sleep(9)
	getHostsViaJustPingAndping6It(tNum)
elif mode=='1':
	print 'getHostsViaJustPing(%s,updateAll=0)' % tNum
	time.sleep(9)
	getHostsViaJustPing(tNum,updateAll=0)
elif mode=='2':
	print 'getHostsViaJustPing(%s,updateAll=1)' % tNum
	time.sleep(9)
	getHostsViaJustPing(tNum,updateAll=1)
elif mode=='3':
	print 'ping6FromFile(%s,updateAll=0)' % tNum
	time.sleep(9)
	ping6FromFile(tNum,updateAll=0)
elif mode=='4':
	print 'ping6FromFile(%s,updateAll=1)' % tNum
	time.sleep(9)
	ping6FromFile(tNum,updateAll=1)

#ping6FromFile(50,updateAll=1)
#getHostsViaJustPing(20,updateAll=1)
#getHostsViaJustPingAndping6It(tNum)

