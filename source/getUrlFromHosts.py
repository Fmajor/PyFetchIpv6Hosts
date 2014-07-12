import pickle,sys,os

if len(sys.argv)>1:
	hostsName = sys.argv[1]
	print 'hostsName is ', hostsName
else:
	hostsName = 'hosts'
	print 'hostsName is ', hostsName

urlFilePath = 'inputHosts/' + hostsName

with open(urlFilePath,'r') as f:
	eachLines=[eachLine.split('#')[0].rstrip().split('/')[0] for eachLine in f if len(eachLine.split('#')[0].rstrip())>0]

urls = [each.split()[1] for each in eachLines]

hostsHeaderNum = 9
urls = urls[9:]

with open('urlFiles/allUrls.txt','w') as f:
	for eachUrl in urls:
		f.write(eachUrl+'\n')
