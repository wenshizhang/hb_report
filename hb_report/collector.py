#!/usr/bin/python3.5
# _*_ coding: utf-8 _*_
# File Name: collector.py
# mail: wenshizhang555@hoxmail.com
# Created Time: Thu 27 Oct 2016 01:23:13 PM CST
# Description:
#########################################################################
import	os
import	envir
import	sys
import	socket

from	node import	node

class collector(node):


	def collect_info(self):
		pass

	def return_result(self):
		pass

	def get_envir(self):
		pass
	
	def __init__(self):
		pass


def run():
	sla = collector()
	
	#who am i
	sla.WE = socket.gethostname()

	#get WORKDIR
	sla.WORKDIR = sla.mktemp()
	sla.WORKDIR = sla.WORKDIR+"/"+sla.WE
	print sla.WORKDIR


run()

