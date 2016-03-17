#!/usr/bin/python
from pubsub import pub
import json as js
from publishers.TwitterClient import Client
from PyQt4 import QtGui, QtCore
from fscUI.fscEntry import fscEntry              
from fscUI.fscTab import fscTab 
from fscUI.fscWindow import fscWindow
import sys
import os
import datetime
import glob
import re
import publishers
import subscribers
import messages
import datetime
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

# def read_file(file):
		# #file = glob.glob(file+'*.json')
		# if(os.path.exists('data/'+file)):
			# with open(os.path.join('data/' , file), encoding='utf-8') as f:
				# try:
					# return js.load(f)
				# except ValueError:
					# print('ValueError')
		# else :
			# print("There is no /data directory available to fsc in the working directory or the required file has been deleted.")

# test_data = read_file('raw_trump_2016_03_07_12_14_02.json')

# app	= QtGui.QApplication(sys.argv)

# tabs = QtGui.QTabWidget()
# app.setActiveWindow(tabs)
# tabs.setWindowTitle("fsc")
# tab = QtGui.QWidget(tabs)
# tab_layout = QtGui.QVBoxLayout()
# content = QtGui.QWidget(tab)
# content_layout = QtGui.QVBoxLayout(content)


# fscE = []
# for x in range(len(test_data)-1): 
	# a = fscEntry(test_data[x])
	# b = QtGui.QLabel(str(x))
	# fscE.append([a,b])
	# content_layout.addWidget(a)
# tab.setLayout(tab_layout)

# fun = QtGui.QWidget(tab)
# sub = QtGui.QWidget(tab)
# fun_layout = QtGui.QVBoxLayout()
# fun.setLayout(fun_layout)
# a = QtGui.QLabel(fun)
# a.setText('ahhhhhhh')
# fun_layout.addWidget(a)

# for a in range(4):
	# b = QtGui.QLabel(fun)
	# b.setText('yay')
	# fun_layout.addWidget(b)
# scroll = QtGui.QScrollArea(tab)
# scroll.setWidget(content)
# scroll.setWidgetResizable(True)
# tab_layout.addWidget(scroll)

# text = QtGui.QTextEdit(fun)
# fun_layout.addWidget(text)
# if(text.toPlainText() is ''):
	# text.insertHtml('YAAAAAAAAAAAAAY')
# else:
	# text.insertHtml('FUCK')
	
from pubsub import pub

# def funfun(arg1):
	# print('thank fucking god' + arg1)
# pub.subscribe(funfun, 'please')
# pub.sendMessage('please', arg1="findme")
# while(True):
	# pub.sendMessage('please', arg1="find me")



#subbly = subscribers.TwitterSubscriber.TwitterSubscriber('standard', 'trump', sub)
pubbly = publishers.TwitterPublisher.TwitterPublisher('standard', 'trump')
#print('completed')
#for lbl in reversed(range(fun_layout.count())):
#	w = fun_layout.takeAt(lbl)
#	if w is not None:
#		w = w.widget()
#		w.deleteLater()

