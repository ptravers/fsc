#!/usr/bin/python
from pubsub import pub
import json as js
from publishers.TwitterClient import Client
from PyQt4 import QtGui
from PyQt4 import QtCore
import sys
import os
import datetime
import glob




API_KEY, API_SECRET = ('5jquzflYqTUNMNqmpdxPUr4Si', 'RE3tNfpjyhNB5IJatzLiDnoonEw7i2OgWz0o5kSCbS2egllDBv')

class StandardMessage():
	def __init__(self):
		self.shares = "null"
		self.likes = "null"
		self.node = "null"
		self.comment = "null"
		self.url = "null"
		self.hashtags = "null"
		self.mentions = "null"
		self.shared = "null"
		self.id = "null"
		self.followers = "null"
		self.following = "null"
		
	def get_dict(self):
		return self.__dict__
	
	def get_message(self):
		return js.dumps(self.__dict__, sort_keys=True, indent=4, separators=(',', ':'))
	def get_comment(self):
		return self.comment

		
class Main_Gui:
	def __init__(self):
		app	= QtGui.QApplication(sys.argv)
		tabs = fscWindow()
		tab	= QtGui.QWidget()
		sub = TwitterSubscriber('standard', 'Trump', tab)
		pub = TwitterPublisher('standard', 'Trump')


class TwitterPublisher:
	def __init__(self, message, term):
		self.client = Client(API_KEY, API_SECRET)
		self.message_type = message
		self.search_term = term

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
			output.get('statuses')[x]['text']
			msg.shared = str(output.get('statuses')[x]['retweeted'])
			msg_array.append(msg)
		return msg_array
	
	def get_rate(self):
		i = self.client.rate_limit_status()['resources']['search']
		return i
	
	def run(self):
		msg = self.get_data(100)
		pub.sendMessage(self.search_term, arg1=msg)
		
		
		
class fscWindow(QtGui.QTabWidget):
	
	def __init__(self):
		super.__init__()
		self.setWindowTitle('FSC')
		self.createMainTab()
	
		
	def create_main_tab(self):
		layout = QtGui.QVBoxLayout()
		search_box = QWidget(self)
		search_box_layout = QHBoxLayout(search_box)
		text_entry = QLineEdit(search_box)
		
		search_box_layout.addWidget(text_entry)
		
	

class tabDropDown(QtGui.QWidget):
	def __init__(self):
		super().__init__()
		#add box for this hbox
		self.publisher_menu = QtGui.QComboBox(self)
		self.subscriber_menu = QtGui.QComboBox(self)
		self.layout = QHBoxLayout(self)
		self.setLayout(self.layout)
		self.imports = []
		#self.publisher_menu.activated[str].connect(self.run_publisher)
		#self.subscriber_menu.activated[str].connect(self.run_subscriber)
		#impliment the publisher calls here?
		
	def populate_menus(self):
		if(os.path.isdir('publishers') and os.path.isdir('subscribers')):
			pubs = glob.glob('publishers/*Publisher.py')
			self.add_items_to_menu(pubs, self.publisher_menu)
			
			subs = glob.glob('subscribers/*Subscriber.py')
			self.add_items_to_menu(subs, self.subscriber_menu)
			
			self.layout.addWidget(self.publisher_menu)
			self.layout.addWidget(self.subscriber_menu)
		else:
			print("No directory Publishers or no directory Subscriber.")
	
	def add_items_to_menu(self, items, menu):
		for x in range(0, len(items)):
			b = items[x].split('\\')[1].split('.')[0]
			self.imports.append([items[x].split('\\')[0],b])
			menu.addItem(b)
			
	def run_publisher(self):
		return True
		#add code to create drop down showing all publishers and subscribers that can be used.

class fscEntry(QtGui.QWidget):
	def __init__(self, data_object):
		super.__init__()
		self.layout = QtGui.QHBoxLayout()
		self.data_layout = QtGui.QHBoxLayout()
		self.data = data_object
		self.input_box = QTextEdit()
		self.data_layout.addWidget(self.input_box)
		self.output_box = QtGui.QWidget()
		self.output_layout = QtGui.QVBoxLayout(self.output_box)
		self.populate_output()
		self.output_box.setLayout(self.output_layout)
		self.data_layout.addWidget(self.output_box)
		
	
	def populate_output(self):
		dict_ = json.loads(self.data)
		for key in dict_.keys():
			entry = QtGui.QWidget(self.output_box)
			entry_layout = QtGui.QHBoxLayout(entry)
			entry_layout.addWidget(QtGui.QLabel(self.output_box).setText)
			temp = QtGui.QTextEdit(self.output_box).setLineWrapMode(QtGui.QTextEdit.NoWrap)
			temp.setReadOnly(True)
			temp.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
			entry_layout.addWidget(temp.insertHtml(dict_[key]))
			output_layout.addWidget(entry)

class fscTab(QtGui.QWidget):
	def __init__(self, search_term, message_type, layout=None):
		super.__init__()
		if(not layout):
			self.primary_layout =  QtGui.QVBoxLayout(self)
			self.primary_layout.addWidget(tabDropDown())
			
	
	
def main():
	fscraper = QApplication(sys.argv)
	primary_window = fscWindow()
	primary_window.show()
	primary_window.raise_()
	fscraper.exec_()

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
			self.scroll = QtGui.QScrollArea(self.parent_window)
			self.tab_layout = QtGui.QGridLayout()

		pub.subscribe(self.listener, self.topic_name)
	
	def update_frame(self):
		
		if(self.window):
			self.update_file(self.file_name, self.current_data)
			self.tab_layout.setSpacing(3)
			self.window.setLayout(self.tab_layout)
			self.scroll.setWidget(self.window)
			self.scroll.setWidgetResizable(True)
			layout = QtGui.QVBoxLayout(self.parent_window)
			layout.addWidget(self.scroll)
			for row in range(len(self.current_data)):
				input_box = QtGui.QTextEdit()
				input_box.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
				
				output_box = QtGui.QTextEdit(self.window)
				output_box.setLineWrapMode(QtGui.QTextEdit.NoWrap)
				output_box.setReadOnly(True)
				output_box.insertHtml(str(self.current_data[row]))
				
				self.text_input_areas.append(output_box)
				
				self.tab_layout.addWidget(input_box,row,1)
				self.tab_layout.addWidget(output_box,row,0)


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
			msg_array = create_output(msg_array)
		with open('data/'+file, 'w', encoding='utf-8') as f:
			js.dump(msg_array, f)
	
	def name_file(self, primary_name):
		return str(primary_name) + "_" + str(datetime.datetime.now()).replace("-", "_").replace(" ", "_").replace(":","_").split(".")[0] + ".json"
	
	def listener(self, arg1):
		self.twitter_call_limit.append(arg1[0])
		arg1 = arg1[1:]
		for x in range(len(arg1)):
			arg1[x] = arg1[x].get_dict()
		self.raw_data += arg1
		self.current_data += arg1
		self.update_file(self.raw_file_name, self.raw_data)
		self.update_frame()




app	= QtGui.QApplication(sys.argv)

tabs	= QtGui.QTabWidget()
app.setActiveWindow(tabs)
tabs.setWindowTitle("fsc")

tab	= QtGui.QWidget(tabs)

sub = TwitterSubscriber('standard', 'Trump', tab)
pub = TwitterPublisher('standard', 'Trump')

tabs.addTab(sub.parent_window, sub.topic_name)

#Resize width and height
tabs.resize(600, 600)
    
#Move QTabWidget to x:300,y:300
tabs.move(300, 300)
  
tabs.show()
    
sys.exit(app.exec_())

