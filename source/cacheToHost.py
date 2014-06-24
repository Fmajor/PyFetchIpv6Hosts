import pickle,sys,os

if len(sys.argv)>1:
	urlFileName=sys.argv[1]
	print 'urlFileName is ',urlFileName
else:
	urlFileName = 'url.txt'
	print 'urlFileName is ',urlFileName

cacheFileName = 'data/'+urlFileName+'.cache.dat'

if not os.path.exists(cacheFileName):
	raise ValueError, 'no file'

with open(cacheFileName,'r') as f:
	finished = pickle.load(f)

N=len(finished[0])
toWriteList = [[],[]]
toWriteList[0]=[finished[0][i] for i in range(N) if len(finished[1][i])>0]
toWriteList[1]=[finished[1][i] for i in range(N) if len(finished[1][i])>0]

def list2host(oneList):
	tN = len(oneList[0])
	with open('generatedHosts/'+'myhostOf%s'%(urlFileName),'w') as f:
		for i in range(tN):
			f.write(toWriteList[1][i] + '\t\t\t'  + toWriteList[0][i] + '\n')	

list2host(toWriteList)
