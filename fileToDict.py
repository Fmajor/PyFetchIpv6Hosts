import os
import pickle

dataPath = 'data/eachURLdata'
if not os.path.exists(dataPath):
	raise ValueError,"no file"
os.chdir(dataPath)

files = os.listdir('.')
urls = [eachUrl[:-4] for eachUrl in files]
N = len(files)

dataList = [[],[]]

for i in range(N):
	with open(files[i],'r') as f:
		temDict = pickle.load(f)
		dataList[0].append(urls[i])
		dataList[1].append(temDict[urls[i]]) 
