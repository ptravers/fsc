#!/usr/bin/python
from pubsub import pub
import json as js
from PyQt4 import QtGui,QtCore
import os
import datetime
from fscUI.fscEntry import fscEntry

class TwitterSubscriber:
	def __init__(self, msg_type, topic_name, window=None):
		self.topic_name = str(topic_name)
		self.msg_type = msg_type
		self.twitter_call_limit = []
		self.raw_file_name = "raw_" + self.name_file(topic_name)
		self.file_name = self.name_file(topic_name)
		self.text_input_areas = []
		self.current_data = []
		self.raw_data= []
		self.parent_window = window
		if(self.parent_window):
			self.window = QtGui.QWidget(self.parent_window)
			self.window_layout = QVBoxLayout(self.window)
			self.window.setLayout(self.window_layout)
			self.scroll = QtGui.QScrollArea(self.parent_window)
			self.scroll.setWidget(self.window)
			self.scroll.setWidgetResizable(True)
			self.parent_window.create_new_layout.addWidget(self.window)
		#binds the subscriber so that it doesn't get garbage collected before data is retrieved
		hard_bind = pub.subscribe(self.listener, 'trump')

	def update_frame(self):
		if(self.window):
			


	def get_data_from_UI(self):
		output_areas = []
		for box in self.text_input_areas:
			output_areas.append(box.toPlainText())
		return output_areas

	def read_file(self, file):
		#file = glob.glob(file+'*.json')
		if(os.path.exists('data/'+file)):
			with open(os.path.join('data/' , file), encoding='utf-8') as f:
				return js.load(f)
		else :
			print("There is no /data directory available to fsc in the working directory or the required file has been deleted.")

	def create_output(self, msg_array):
		ui_data = self.get_data_from_UI()
		x = 0
		msg_file = []
		for msg in msg_array:
			msg.node = ui_data[x]
			x += 1
			msg_file.append(msg.__dict__)
		return msg_file

	def update_file(self, file, msg_array):
		if(not msg_array == self.raw_data):
			msg_array = self.create_output(msg_array)
		with open('data/'+file, 'w', encoding='utf-8') as f:
			js.dump(msg_array, f)

	def name_file(self, primary_name):
		return str(primary_name) + "_" + str(datetime.datetime.now()).replace("-", "_").replace(" ", "_").replace(":","_").split(".")[0] + ".json"

	def listener(self, arg1):
		print('arrived')
		self.twitter_call_limit.append(arg1[0])
		arg1 = arg1[1:]
		for x in range(len(arg1)):
			arg1[x] = arg1[x].get_dict()
		self.raw_data += arg1
		self.current_data += arg1
		self.update_file(self.raw_file_name, self.raw_data)
		self.update_frame()
