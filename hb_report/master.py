#!/usr/bin/python3.5
# _*_ coding: utf-8 _*_
# File Name: get_second.py
# mail: wenshizhang555@hoxmail.com
# Created Time: Wed 26 Oct 2016 11:28:22 AM CST
# Description:
#########################################################################
import datetime

from crmsh import logtime
from crmsh import utils
from crmsh import logparser
from envir import envir

class master:
	SUDO = ''
	LOCAL_SUDO = ''
	ENVIRONMENT = ''

	def __init__(self,envir):
		self.ENVIRONMRNT = envir

	def analyzed_argvment():
		pass

	def mktemp(self,s):
		pass

	def is_node():
		pass

	def find_ssh_user():
		pass

	def find_sudo():
		pass

	def change_time():
		pass

	def collect_for_nodes():
		pass

	def start_collect():
		pass

	def analyzed():
		pass

	def events():
		pass

	def check_if_log_is_empty():
		pass

	def final_word():
		pass

	def send_envir():
		pass

	def run():
		'''
		This method do most of the job that master node should do
		'''
		pass



env = envir()
mtr = master(env)
mtr.run()
