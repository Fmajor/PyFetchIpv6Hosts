import re,sys,os
import pdb


if len(sys.argv)>1:
	dataName = sys.argv[1]
else:
	dataName = 'httpfox.dat'

f = open(dataName,'r')
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
	urlSet.update(oldUrlData)

f = open(outName,'w')
toWriteList = list(urlSet)
toWriteList.sort()
for eachUrl in toWriteList:
	f.write(eachUrl + '\n')

f.close()
