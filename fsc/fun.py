#!/usr/bin/python
from pubsub import pub
import json as js
from publishers.TwitterClient import Client
from PyQt4 import QtGui, QtCore
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



app	= QtGui.QApplication(sys.argv)

tabs = QtGui.QTabWidget()
app.setActiveWindow(tabs)
tabs.setWindowTitle("fsc")
tab = QtGui.QWidget

fun = QtGui.QWidget()
sub = QtGui.QWidget()
fun_layout = QtGui.QVBoxLayout()
fun.setLayout(fun_layout)
a = QtGui.QLabel(fun)
a.setText('ahhhhhhh')
fun_layout.addWidget(a)
for a in range(4):
	b = QtGui.QLabel(fun)
	b.setText('yay')
	fun_layout.addWidget(b)


text = QtGui.QTextEdit(fun)
fun_layout.addWidget(text)
if(text.toPlainText() is not ''):
	text.insertHtml('YAAAAAAAAAAAAAY')
else:
	text.insertHtml('FUCK')
	
from pubsub import pub

# def funfun(arg1):
	# print('thank fucking god' + arg1)
# pub.subscribe(funfun, 'please')
# pub.sendMessage('please', arg1="findme")
# while(True):
	# pub.sendMessage('please', arg1="find me")

	
subbly = subscribers.TwitterSubscriber.TwitterSubscriber('standard', 'trump', sub)
pubbly = publishers.TwitterPublisher.TwitterPublisher('standard', 'trump')
print('completed')
tabs.addTab(sub, 'sub')
tabs.addTab(fun, 'fun')
tabs.show()

#for lbl in reversed(range(fun_layout.count())):
#	w = fun_layout.takeAt(lbl)
#	if w is not None:
#		w = w.widget()
#		w.deleteLater()

sys.exit(app.exec_())