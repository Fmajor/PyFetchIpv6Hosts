import re,sys,os
import pdb


if len(sys.argv)>1:
	dataName = sys.argv[1]
	dataPath = 'updateHosts/' + dataName
else:
	dataName = 'httpfox.dat'
	dataPath = 'updateHosts/' + dataName

f = open(dataPath,'r')
data = f.read()
f.close()

outName = 'urlFiles/url.txt'
urlData = re.findall(r"://(.*?.googlevideo.com)/",data)
urlSet = set(urlData)
if os.path.exists(outName) and os.path.getsize(outName)>0:
	oldUrlData = []
	with open(outName,'r') as f:
		for eachUrl in f:
			oldUrlData.append(eachUrl[:-1]) 
	oldNum = len(oldUrlData)
	urlSet.update(oldUrlData)
	newNum = len(urlSet)
	print (newNum - oldNum),'urls updated'

f = open(outName,'w')
toWriteList = list(urlSet)
toWriteList.sort()
for eachUrl in toWriteList:
	f.write(eachUrl + '\n')

f.close()
