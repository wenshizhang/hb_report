#!/usr/bin/python3.5
# _*_ coding: utf-8 _*_
# File Name: node.py
# mail: wenshizhang555@hoxmail.com
# Created Time: Thu 27 Oct 2016 11:11:28 AM CST
# Description:
#########################################################################
import	os
import	tempfile
import	envir
import	utillib

class node:
	SSH_PASSWD = ''
	WE = ''
	WORKDIR = ''
	THIS_IS_NODE = ''

	def mktemp(self):
		tmpdir = tempfile.mkdtemp()
		return tmpdir

	def get_crm_daemon_dir(self):
		'''
		Get envir.CRM_DARMON_DIR
		'''
		libdir = utillib.dirname(envir.HA_BIN)

	def get_crm_daemon_dir2(self):
		'''
		Get_crm_daemon_dir function failed
		'''

	def compabitility_pcmk(self):
		self.get_crm_daemon_dir() or self.get_crm_daemon_dir2()

	def high_debug_level1(self):
		pass

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


