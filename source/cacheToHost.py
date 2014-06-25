import pickle,sys,os,commands
import pdb

def sortRows(theList,rowNum):
	N = len(theList)
	eachN = len(theList[0])
	indices = range(eachN)
	indices.sort(key = theList[rowNum].__getitem__)
	result=[[] for i in range(N)]
	for i, sublist in enumerate(theList):
		result[i] = [sublist[j] for j in indices]
	return result

def list2host(oneList,filePath):
	tN = len(oneList[0])
	with open(filePath, 'w') as f:
		f.write('# generated by PyFetchIpv6Hosts\n')
		for i in range(tN):
			f.write(toWriteList[1][i] + '\t\t\t'  + toWriteList[0][i] + '\n')	

def processOneFile(cacheFileName):
	if not os.path.exists(cacheFileName):
		raise ValueError, 'no file'

	with open(cacheFileName,'r') as f:
		finished = pickle.load(f)

	N=len(finished[0])
	toWriteList = [[],[]]
	toWriteList[0]=[finished[0][i] for i in range(N) if len(finished[1][i])>0]
	toWriteList[1]=[finished[1][i] for i in range(N) if len(finished[1][i])>0]

	return toWriteList

if len(sys.argv)>1:
	urlFileName=sys.argv[1]
	print 'urlFileName is ',urlFileName
else:
	urlFileName = 'url.txt'
	print 'urlFileName is ',urlFileName

if urlFileName == 'all':
	cacheFileNames = os.listdir('data')
	cacheFileNames = [each for each in cacheFileNames if each.find('.dat')>0]
	N = len(cacheFileNames)
	toWriteDict = {}
	for i in range(N):
		tempLists = processOneFile('data/'+cacheFileNames[i])
		listNum = len(tempLists[0])
		for i in range(listNum):
			toWriteDict.update({tempLists[0][i]:tempLists[1][i]})

	toWirteNum = len(toWriteDict)
	toWriteList = [[],[]]
	for eachKey in toWriteDict.keys():
		toWriteList[0].append(eachKey)
		toWriteList[1].append(toWriteDict[eachKey])

	toWriteList = sortRows(toWriteList,0)# sort by url
	filePath = '../hosts.bnu'
	(status, output) = commands.getstatusoutput('cp '+filePath+' backups/')
	list2host(toWriteList,filePath)

else:
	cacheFileName = 'data/'+urlFileName+'.cache.dat'
	toWriteList = processOneFile(cacheFileName)
	filePath = 'generatedHosts/'+'myhostOf%s'%(urlFileName)
	list2host(toWriteList, filePath)

