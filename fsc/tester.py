#!/usr/bin/python
from pubsub import pub
import json as js
import publishers
import subscribers
import messages
from PyQt4 import QtGui, QtCore
import sys
import os
import datetime
import glob
import re
regex = re.compile(r'(?!__)([A-Za-z])*(?!__)')

def import_all(import_files):
	check = import_files[len(import_files)-1]
	for x in range(len(import_files)-1):
		module = import_files[x].split('.')[0]
		if(check == 0):
			__import__('publishers.'+module)
		elif(check == 1):
			__import__('subscribers.'+module)
		else:
			__import__('messages.'+module)

import_all(list(filter(regex.match, os.listdir('publishers')))+[0])
import_all(list(filter(regex.match, os.listdir('subscribers')))+[1])
import_all(list(filter(regex.match, os.listdir('messages')))+[2])



def main():
	fscraper = QtGui.QApplication(sys.argv)

	primary_window = fscWindow()
	fscraper.setActiveWindow(primary_window)
	primary_window.show()
	primary_window.raise_()
	fscraper.exec_()

def funfun(arg1):
	print('thank fucking god' + arg1[2].get_message())
# pub.subscribe(funfun, 'please')
# pub.sendMessage('please', arg1="findme")
# while(True):
	# pub.sendMessage('please', arg1="find me")

app	= QtGui.QApplication(sys.argv)
plubbt = pub.subscribe(funfun, 'trump')
fscWindow(app)
