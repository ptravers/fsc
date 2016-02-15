#!/usr/bin/python
from pubsub import pub
import json as js
from application_only_auth import Client
from PyQt4 import QtGui
from PyQt4 import QtCore
import sys
import os
import datetime


API_KEY, API_SECRET = ('5jquzflYqTUNMNqmpdxPUr4Si', 'RE3tNfpjyhNB5IJatzLiDnoonEw7i2OgWz0o5kSCbS2egllDBv')

class StandardMessage():
	def __init__(self):
		self.shares = "null"
		self.likes = "null"
		self.nodes = []
		self.comment = "null"
		self.url = "null"
		self.hashtags = "null"
		self.mentions = "null"
		self.shared = "null"
		self.id = "null"
		
	def get_message(self):
		return js.dumps(self.__dict__, sort_keys=True, indent=4, separators=(',', ':'))

		
class Main_Gui():
	def __init__(self):
		app	= QtGui.QApplication(sys.argv)
		tabs	= QtGui.QTabWidget()
		tabs.setWindowTitle("fsc")
		tab	= QtGui.QWidget()
		sub = TwitterSubscriber('standard', 'Trump', tab)
		pub = TwitterPublisher('standard', 'Trump')


class TwitterPublisher:
	def __init__(self, message, term):
		self.client = Client(API_KEY, API_SECRET)
		self.message_type = message
		self.search_term = term
		self.topic_name = term + "_" + str(datetime.datetime.now()).replace("-", "_").replace(" ", "_").replace(":","_").split(".")[0]
		self.search_link_base = 'https://api.twitter.com/1.1/search/tweets.json?q='
		self.link_base = 'https://twitter.com/'
		self.run()
	
	#Get rate limit when the rate limit is less than the count given the system
	#must request rate_limit. Then enter waiting state
	
	def get_data(self, count):
		search_link = self.search_link_base + self.search_term + "&count=" + str(count)
		output = self.client.request(search_link)
		msg_array = []
		msg_array.append(self.get_rate())
		for x in range(len(output.get('statuses'))):
			msg = StandardMessage()
			msg.mentions = output.get('statuses')[x]['entities']['user_mentions']
			msg.id = output.get('statuses')[0]['id_str']
			msg.shares = str(output.get('statuses')[x]['retweet_count'])
			msg.likes = str(output.get('statuses')[x]['favorite_count'])
			msg.hashtags = output.get('statuses')[x]['entities']['hashtags']
			msg.url = self.link_base + output.get('statuses')[x]['user']['screen_name'] + '/status/' + msg.id
			msg.comment = str(output.get('statuses')[x]['text'])
			msg.shared = str(output.get('statuses')[x]['retweeted'])
			msg_array.append(msg)
		return msg_array
	
	def get_rate(self):
		i = self.client.rate_limit_status()['resources']['search']
		return i
	
	#This should be placed in the Parent class should be passed a message a string and the publisher object
	def run(self):
		msg = self.get_data(400)
		pub.sendMessage(self.search_term, arg1=msg)
		

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
				output_box = QtGui.QTextEdit(self.window)
				output_box.setReadOnly(True)
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
		
		



app	= QtGui.QApplication(sys.argv)
tabs	= QtGui.QTabWidget()
tabs.setWindowTitle("fsc")
tab	= QtGui.QWidget()
sub = TwitterSubscriber('standard', 'Trump', tab)
pub = TwitterPublisher('standard', 'Trump')
tabs.addTab(sub.parent_window, sub.topic_name)
#vBoxlayout	= QtGui.QVBoxLayout()
#vBoxlayout.addWidget(pushButton1)
#vBoxlayout.addWidget(pushButton2)

#Resize width and height
tabs.resize(600, 600)
    
#Move QTabWidget to x:300,y:300
tabs.move(300, 300)
    
#Set Layout for Third Tab Page
#tab3.setLayout(vBoxlayout)   
    
#tabs.addTab(tab1,"Tab 1")
#tabs.addTab(tab2,"Tab 2")
#tabs.addTab(tab3,"Tab 3")
    
tabs.show()
    
sys.exit(app.exec_())

