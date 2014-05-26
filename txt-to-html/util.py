# -*- coding:utf-8 -*-

'util.py'

class Rule :
	"""
	定义一些规则，对于不同的块，根据不同的规则去定义这个块的所属
	下面只是应用了一些简单的规则，具体的可以自己去定义
	"""
	def action (self , block , handler) :
		handler.start (self.type)
		handler.feed (block)
		handler.end (self.type)
		return True

class HeadingRule (Rule) :
	"""
	标题单独占一行，最多70个字符，而且不以冒号结尾
	"""
	type = 'heading'
	def condition (self , block) :
		return not '\n' in block and len (block) <= 70 and not block[-1] == ':'

class TitleRule (HeadingRule) :
	"""
	题目是文档的第一个块，而且是个标题
	"""
	type = 'title'
	first = True

	def condtion (self , block) :
		if not self.first :
			return False
		self.first = False
		return HeadingRule.condition (self , block)

class ListItemRule (Rule) :
	"""
	列表项是以连字符开始的段落
	"""
	type = 'listitem'
	def condition  (self , block) :
		return block[0] == '-'
	def action (self , block , handler) :
		handler.start (self.type)
		handler.feed (block[1:].strip ())
		handler.end (self.type)
		return True

class ListRule (ListItemRule) :
	"""
	列表就是包括一些连续的列表项
	"""
	type = 'list'
	inside = False
	def condition (self , block) :
		return True
	def action (self , block , handler) :
		if not self.inside and ListItemRule.condition (self , block) :
			handler.start (self.type)
			self.inside = True
		elif self.inside and not ListItemRule.condition (self , block) :
			handler.end (self.type)
			self.inside = False
		return False

class ParagraphRule (Rule) :
	"""
	除了以上特殊规则，则视为段落
	"""
	type = 'paragraph'
	def condition (self , block) :
		return True