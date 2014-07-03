#-*-coding:utf-8-*-
import re
import urllib
import urllib2
import HTMLParser
import cookielib
import sys
import string 

class POJLogin :
	'''
	登录POJ
	'''
	def __init__ (self , user , password) :
		self.hosturl = r'http://poj.org/problemlist'
		self.posturl = r'http://poj.org/login'
		self.headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:29.0) Gecko/20100101 Firefox/29.0' , 'Refer': 'http://poj.org/'}
		self.user = user
		self.password = password
		self.postData = {'user_id1' : self.user , 'password1' : self.password , 'B1': 'login' , 'url' : '/'}
        
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
	'''
	def __init__ (self , user , password) :
		self.user = user
		self.password = password
		self.main ()

	def login (self) :
		self.pojlogin = POJLogin (self.user , self.password)
		self.pojlogin.main ()

	def HTMLtoID (self , html) :
		rule = r'<td>(\d{7,8})</td>'
		st = re.compile (rule)
		return re.findall (st , html)

	def getRealCode(self , html):
		rule = r'style="font-family:Courier New,Courier,monospace">([\d\D]*)</pre>'
		re.compile(rule)
		return re.findall(rule,html)

	def getSolutionID (self) :
		ID = []
		Last = 111111111   
		while True :
			url = 'http://poj.org/status?user_id=' + self.user + '&result=0&language=&top=' + str (Last)
			request = urllib2.Request (url)
			response = urllib2.urlopen (request)
			html = response.read ()
			thispage = self.HTMLtoID (html)
			if len (thispage) == 0 :
				break 
			Last = thispage[-1]
			ID = ID + thispage
		return ID

	def getProblemID (self , html) :
		rule = r'>(\d{4})<'
		st = re.compile (rule)
		problem = re.findall (st , html)
		return problem[0]

	def getLangluage (self , html) :
		rule = r'Language:</b> ([\D]*)</td><td width=10px>'
		st = re.compile (rule)
		language = re.findall (st , html)
		if language[0] == 'G++' or language[0] == 'C++' : return '.cpp'
		elif language[0] == 'Java' : return '.java'
		elif language[0] == 'GCC' or language[0] == 'C' : return '.c'
		else : return '.txt'

	def getCode (self , AcceptID) :
		dic = [0 for i in range (10000)]
		for ID in AcceptID :
			url = 'http://poj.org/showsource?solution_id=' + ID
			page = urllib2.urlopen (urllib2.Request (url))
			file = page.read ()
			txt = self.getRealCode (HTMLParser.HTMLParser ().unescape (file))
			problemID = self.getProblemID (file)
			dic[int (problemID)] += 1
			name = 'poj_' + problemID
			if dic[int (problemID)] != 1 :
				name = name + '_' + str (dic[int (problemID)])
			with open (name + self.getLangluage (file) , 'w') as out :
				for line in txt:
					out.write (line)

	def main (self) :
		self.login ()
		AcceptID = self.getSolutionID ()
		self.getCode (AcceptID)


if __name__ == '__main__' :
	reload(sys)
	sys.setdefaultencoding('utf8')
	poj = Spider ('cxlove' , '5571645')

