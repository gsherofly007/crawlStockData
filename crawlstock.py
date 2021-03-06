#-*- coding:utf8 -*-
import urllib2
import os
import time
import thread

def checkDirectory(directory):
	if(not os.path.exists(directory)):
		os.mkdir(directory)

def checkfile(filepath):
	if(os.path.exists(filepath)):
		f = open(filepath,"r")
		data = f.read()
		f.close()
		if(len(data) == 0 or len(data) == 82):
			return True
		else:
			print "file length:"+str(len(data))
			return False
	else:
		return True
def crawlStock(date,dateRoot,code,srcUrl,sYear,sMonth,sDay):
	dYear = 2015
	dMonth = 6
	dDay = 1
	if(sYear == dYear and sMonth == dMonth and sDay > dDay):
		print "time out"
		return 
	elif(sYear == dYear and sMonth > dMonth):
		print "time out"
		return
	else:
		pass
	fileName = dateRoot+"/"+date+"_"+code+".xls"
	if(not checkfile(fileName)):
		return 
	url = srcUrl + date + "&symbol=" + code
	print(url)
	data = ""
	try:
		f = urllib2.urlopen(url,data=None,timeout=15)
		data = f.read()
	except:
		data = ""

	print "data size:"+str(len(data))
	if(len(data)==0 or len(data)==82):
		f = open("error","a+")
		f.write(code+" "+date+"\r\n")
		f.close()
	print(fileName)
	f = open(fileName,'w')
	f.write(data)
	f.close()

def  readLinesOfFile(filepath):
	try:
		f = open(filepath,'r')
	except Exception, e:
		raise e
	finally:
		allLines = f.readlines()
		codelist = []
		for line in allLines:
			codelist.append(line[0:6])
		return codelist

def mainCrawl(sYear,sMonth,sDay,codeList,root,code):
	srcUrl = "http://market.finance.sina.com.cn/downxls.php?date="
	list31day = [1,3,5,7,8,10,12]
	dYear = 2016
	codeIndex = codeList.index(code)
	codeListLen = len(codeList)
	while codeIndex < codeListLen:
		codeName = root + codeList[codeIndex]
		codeRoot = root+"/"+codeList[codeIndex]
		checkDirectory(codeRoot)
		codeIndex += 1
		while sYear < dYear:
			date1  = str(sYear) + "-"
			while sMonth<13:
				date2 = date1
				if sMonth<10:
					date2 += "0"+str(sMonth)+"-"
				else:
					date2 += str(sMonth)+"-"
				if sMonth in list31day:
					while sDay < 32:
						date3 = date2
						if sDay < 10:
							date3 += "0"+str(sDay)
						else:
							date3 += str(sDay)
						dateRoot = codeRoot+"/"+date3
						checkDirectory(dateRoot)
						crawlStock(date3,dateRoot,codeName,srcUrl,sYear,sMonth,sDay)
						sDay += 1
					sDay =1
				else:
					while sDay < 31:
						date3 = date2
						if sDay < 10:
							date3 += "0"+str(sDay)
						else:
							date3 += str(sDay)
						dateRoot = codeRoot+"/"+date3
						checkDirectory(dateRoot)
						crawlStock(date3,dateRoot,codeName,srcUrl,sYear,sMonth,sDay)
						sDay += 1
					sDay =1
				sMonth += 1
			sMonth =1
			sYear += 1
		sYear = 2014
	return	

#thread function
def threadSH():
	shCodeList = readLinesOfFile('shcode')
	shRoot = 'sh'
	checkDirectory(shRoot)
	mainCrawl(2014,1,1,shCodeList,shRoot,'600000')

def threadSZ():
	szCodeList = readLinesOfFile('szcode')
	szRoot = 'sz'
	checkDirectory(szRoot)
	mainCrawl(2014,1,1,szCodeList,shRoot,"000001")


if __name__ == "__main__":
	try:
		thread.start_new_thread(threadSH,())
		thread.start_new_thread(threadSZ,())
	except:
		pass
	while 1:
		pass
	