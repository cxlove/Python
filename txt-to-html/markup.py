# -*- coding:utf-8 -*-

'markup.py'

import re , sys
from util import *
from rules import *
from handlers import *
class Parser :
	"""
	语法分析器读取文本之后，按块去对应规则处理
	"""
	def __init__ (self , handler) :
		self.handler = handler
		self.rules = []
		self.filters = []
	def addRule (self , rule) :
		self.rules.append (rule)
	def addFilter (self , pattern , name) :
		def filter (block , handler) :
			return re.sub (pattern , handler.sub (name) , block)
		self.filters.append (filter)
	def parse (self , file) :
		self.handler.start ('document')
		for block in blocks (file) :
			# 先对每个块进行过滤
			for filter in self.filters :
				block = filter (block , self.handler)
			# 匹配规则
			for rule in self.rules :
				if rule.condition (block) :
					last = rule.action (block , self.handler)
					if last :
						break
		self.handler.end ('document')

class BasicTextParser (Parser) :
	"""
	对于不同的需求，去添加不同的规则和过滤器
	"""
	def __init__ (self , handler) :
		Parser.__init__ (self , handler)
		self.addRule (ListRule ())
		self.addRule (ListItemRule ())
		self.addRule (TitleRule ())
		self.addRule (HeadingRule ())
		self.addRule (ParagraphRule ())
		
		#三个过滤器，强调、链接、电子邮件
		self.addFilter (r'\*(.+?)\*' , 'emphasis')
		self.addFilter (r'(http://[\.a-zA-Z/]+)' , 'url')
		self.addFilter (r'([\.a-zA-Z]+@[\.a-zA-Z]+[a-zA-Z])' , 'mail')

handler = HTMLRenderer ()
parser = BasicTextParser (handler)
parser.parse (sys.stdin)