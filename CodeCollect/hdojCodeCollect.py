#-*-coding:utf-8-*-
#by cxlove

import re
import urllib
import urllib2
import HTMLParser
import cookielib
import sys
import string 

class HDOJLogin :
	'''
	登录HDOJ
	'''
	def __init__ (self , user , password) :
		self.hosturl = r'http://acm.hdu.edu.cn/'
		self.posturl = r'http://acm.hdu.edu.cn/userloginex.php?action=login'
		self.headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:29.0) Gecko/20100101 Firefox/29.0' , 'Refer': 'http://acm.hdu.edu.cn/'}
		self.user = user
		self.password = password
		self.postData = {'username' : self.user , 'userpass' : self.password , 'login': 'Sign In'}
        
	def main (self) :
		cj = cookielib.LWPCookieJar() 
		cookie_support = urllib2.HTTPCookieProcessor (cj) 
		opener = urllib2.build_opener (cookie_support , urllib2.HTTPHandler)  
		urllib2.install_opener (opener)
		h = urllib2.urlopen (self.hosturl)
		self.postData = urllib.urlencode(self.postData)
		request = urllib2.Request(self.posturl, self.postData , self.headers)  
		response = urllib2.urlopen(request)

class Spider :
	'''
	爬虫
	'''
	def __init__ (self , user , password) :
		self.user = user
		self.password = password
		self.main ()

	def login (self) :
		self.hdojlogin = HDOJLogin (self.user , self.password)
		self.hdojlogin.main ()

	def HTMLtoID (self , html) :
		rule = r'px>(\d{6,8})</td>'
		st = re.compile (rule)
		return re.findall (st , html)

	def getRealCode(self , html):
		rule = r':none;text-align:left;">([\d\D]*)</textarea>'
		re.compile(rule)
		code = re.findall(rule,html)
		return code[0]

	def getSolutionID (self) :
		ID = []
		Last = 111111111   
		while True :
			url = 'http://acm.hdu.edu.cn/status.php?first=' + str (Last - 1) + '&pid=&user=' + self.user + '&lang=0&status=5'
			request = urllib2.Request (url)
			response = urllib2.urlopen (request)
			html = response.read ()
			thispage = self.HTMLtoID (html)
			if len (thispage) == 0 :
				break 
			Last = int (thispage[-1])
			ID = ID + thispage
		return ID

	def getProblemID (self , html) :
		rule = r'target=_blank>(\d{4}) '
		st = re.compile (rule)
		problem = re.findall (st , html)
		return problem[0]

	def getLangluage (self , html) :
		rule = r'Language : ([\D]*)&nbsp;&nbsp;&nbsp;&nbsp;Author'
		st = re.compile (rule)
		language = re.findall (st , html)
		if language[0] == 'G++' or language[0] == 'C++' : return '.cpp'
		elif language[0] == 'Java' : return '.java'
		elif language[0] == 'GCC' or language[0] == 'C' : return '.c'
		else : return '.txt'

	def getCode (self , AcceptID) :
		dic = [0 for i in range (10000)]
		for ID in AcceptID :
			url = 'http://acm.hdu.edu.cn/viewcode.php?rid=' + ID
			page = urllib2.urlopen (urllib2.Request (url))
			file = page.read ()
			txt = self.getRealCode (HTMLParser.HTMLParser ().unescape (file.decode ('gbk')))
			problemID = self.getProblemID (file)
			dic[int (problemID)] += 1
			name = 'hdoj_' + problemID
			if dic[int (problemID)] != 1 :
				name = name + '_' + str (dic[int (problemID)])
			with open (name + self.getLangluage (file) , 'w') as out :
				pre = 0
				for line in txt :
					if line.strip () or line == ' ':
						out.write (line)
						pre = 0
					else :
						if pre == 0 : 
							out.write (line)
						pre = 1

	def main (self) :
		self.login ()
		AcceptID = self.getSolutionID ()
		self.getCode (AcceptID)


if __name__ == '__main__' :
	reload(sys)
	sys.setdefaultencoding('utf8')
	hdoj = Spider ('pythontest' , '123456')

