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
		self.file_name = self.name_file(topic_name)
		self.current_msgs = []
		self.UI_msgs = []
		self.parent_window = window
		try:
			f = open('data/'+self.file_name, 'x')	
			f.close()
		except FileExistsError:
			pass
		if(self.parent_window):
			self.data_area = QtGui.QWidget()
			self.data_area_layout = QtGui.QVBoxLayout(self.data_area)
			self.scroll_area = QtGui.QScrollArea(self.parent_window)
			self.scroll_area.setWidget(self.data_area)
			self.scroll_area.setWidgetResizable(True)
			self.parent_window.main_tab_layout.addWidget(self.scroll_area)
		#binds the subscriber so that it doesn't get garbage collected before data is retrieved
		hard_bind = pub.subscribe(self.listener, topic_name)

	def update_frame(self):
		if(self.parent_window):
			self.update_file(self.file_name, self.current_msgs)
			self.current_msgs = self.read_file(self.file_name)
			for x in range(len(self.UI_msgs), len(self.current_msgs)):
				datum = self.current_msgs[x]
				element = fscEntry(datum)
				self.UI_msgs.append(element)
				self.data_area_layout.addWidget(element)
	
	#get_data_from_UI iterates over a list of input QtextEdit widgets
	#then retrieves whatever is currently written in them
	
	def get_data_from_UI(self):
		output_areas = []
		for box in self.UI_msgs:
			s = box.get_input_data()
			print(s)
			output_areas.append(s)
		return output_areas

	#read_file will load  a file provided it is non empty
	#when read_file loads a file it converts it in to an array of dicts
	#Owing to the structure of the file being that of a json array
	
	def read_file(self, file):
		#file = glob.glob(file+'*.json')
		if(os.path.exists('data/'+file)):
			with open(os.path.join('data/' , file), encoding='utf-8') as f:
				try:
					return js.load(f)
				except ValueError:
					print('ValueError this files is empty or not in the correct json structure')
		else :
			print("There is no /data directory available to fsc in the working directory or the required file has been deleted.")

	#create_output first gets all the data from the UI text areas		
	#then it adds that data to each corresponding dict
	
	def create_output(self, msg_array):
		ui_data = self.get_data_from_UI()
		x = 0
		msg_file = []
		for msg in msg_array:
			msg['node'] = ui_data[x]
			x += 1
			msg_file.append(msg)
		return msg_file
	
	#
	
	def update_file(self,file, msg_array, raw_type=False):
		if(not raw_type and len(self.UI_msgs) == len(msg_array)):
			msg_array = self.create_output(msg_array)
		with open('data/'+file, 'w', encoding='utf-8') as f:
			js.dump(msg_array, f)

	def name_file(self, primary_name):
		return str(primary_name) + "_" + str(datetime.datetime.now()).replace("-", "_").replace(" ", "_").replace(":","_").split(".")[0] + ".json"

	def listener(self, arg1):
		print('data arrived')
		self.twitter_call_limit.append(arg1[0])
		arg1 = arg1[1:]
		for x in range(len(arg1)):
			arg1[x] = arg1[x].get_dict()
		self.current_msgs += arg1
		raw_name = 'raw_'+ self.name_file(self.topic_name)
		self.update_file(raw_name, arg1, raw_type=True)
		self.update_frame()
