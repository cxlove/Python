# -*- coding:utf-8 -*-

'rules.py'

# 按行读入的生成器
def lines (file) :
	for line in file : yield line
	yield '\n'

# 通过空行将文本分块
def blocks (file) :
	block = []
	for line in lines (file) :
		# 如果不是空行，那么加入到块中
		if line.strip () :
			block.append (line)
		elif block :
			# 如果是空行，则生成一个块，然后继续
			yield ''.join (block).strip ()
			block = []
