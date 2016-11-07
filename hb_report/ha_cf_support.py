import os
import sys
import envir
import utillib


def getcfvar(param):
	if not os.path.isfile(envir.CONF):
		return
	
