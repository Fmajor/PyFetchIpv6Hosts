import pickle,sys
if len(sys.argv)>1:
	urlFileName=sys.argv[1]
	print 'urlFileName is ',urlFileName
else:
	urlFileName = 'youtube_and_facebook_url.txt'
	print 'urlFileName is ',urlFileName
cacheFileName = 'data/'+urlFileName+'.cache.dat'

f = open(cacheFileName,'r')
thedict = pickle.load(f)
f.close()
