#!/usr/bin/python3.5
# _*_ coding: utf-8 _*_
# File Name: node.py
# mail: wenshizhang555@hoxmail.com
# Created Time: Thu 27 Oct 2016 11:11:28 AM CST
# Description:
#########################################################################
import os
import tempfile
import envir

class node:
	SSH_PASSWD = ''
	WE = ''
	WORKDIR = ''
	THIS_IS_NODE = ''

	def mktemp(self):
		tmpdir = tempfile.mkdtemp()
		return tmpdir

	def compabitility_pcmk(self):
		os.system(". /usr/lib/ocf/lib/heartbeat/ocf-shellfuncs")
		from heatbeat import ocf-directories

	def get_cluster_type(self):
		pass
	
	def conf(self):
		pass

	def check_this_is_node(self):
		pass

	def getlog(self):
		pass

	def mktar(self):
		pass

