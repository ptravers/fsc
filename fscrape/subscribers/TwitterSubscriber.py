#!/usr/bin/python
from pubsub import pub
import json as js
from PyQt4 import QtGui,QtCore

class TwitterSubscriber:
	def __init__(self, msg_type, topic_name, window=None):
		self.topic_name = str(topic_name)
		self.msg_type = msg_type
		self.parent_window = window
		self.window = QtGui.QWidget(self.parent_window)
		self.raw_output_file = "raw_"+self.topic_name+".txt"
		self.output_file = self.topic_name+".txt"
		self.tab_layout = QtGui.QGridLayout()
		self.twitter_call_limit = []
		if(self.window):
			self.scroll = QtGui.QScrollArea(self.parent_window)
			self.tab_layout = QtGui.QGridLayout()

		pub.subscribe(self.listener, self.topic_name)
	
	def update_frame(self, data):
		if(self.window):
			#current_file = read_file(output_file)
			self.tab_layout.setSpacing(3)
			self.window.setLayout(self.tab_layout)
			self.scroll.setWidget(self.window)
			self.scroll.setWidgetResizable(True)
			layout = QtGui.QVBoxLayout(self.parent_window)
			layout.addWidget(self.scroll)
			for row in range(len(data)):
				input_box = QtGui.QLineEdit()
				input_box.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
				output_box = QtGui.QLabel(self.window)
				#output_box.setReadOnly(True)
				output_box.setText(data[row].get_message())
				self.tab_layout.addWidget(input_box,row,1)
				self.tab_layout.addWidget(output_box,row,0)
			

	def read_raw_file(self):
		self.read_file(self.raw_output_file)
	
	def read_file(self, file):
		if(os.path.exists('data/'+topic_name)):
			with open(os.path.join('data' , '/'+file), encoding='utf-8') as f:
				return js.load(f)
	
	def update_file(self, msg, file):
		with open(file, 'w', encoding='utf-8') as f:
			js.dump(msg, f)
	
	def listener(self, arg1):
		self.twitter_call_limit.append(arg1[0])
		arg1 = arg1[1:]
		self.update_frame(arg1)
		