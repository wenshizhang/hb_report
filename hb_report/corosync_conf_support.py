import os
import sys
import envir
import utillib


def getcfvar(param):
	'''
	function getcfvar parameter need to be list 
	because some place call this function and give two parameters
	and function need to check the number of parameters and to do some different things
	'''
	content=[]
	if not os.path.isfile(envir.CONF):
		return
	f = open(envir.CONF,'r')
	for line in f:
		if line.startswith('#'):
			line = ''
		content = content.append(line)
	
	for i in content:
		print i

def iscfvartrue(param):
	
	print param.split(' ')
	if getcfvar(param.split(' ')):
		#egrep staff
		pass
