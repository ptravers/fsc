#!/usr/bin/python
from pubsub import pub
import json as js
import publishers
import subscribers
import messages
from PyQt4 import QtGui, QtCore
from fscUI.fscWindow import fscWindow
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
	SMK = QtGui.QApplication(sys.argv)
	primary_window = fscWindow(SMK)
	
if __name__ == 'main':
	main()

main()