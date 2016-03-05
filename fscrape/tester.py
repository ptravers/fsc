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


print(getattr(subscribers.TwitterSubscriber, 'TwitterSubscriber'))



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


class fscWindow(QtGui.QTabWidget):

	def __init__(self, parent):
		super().__init__()
		parent.setActiveWindow(self)

		print('creating window')


		self.setWindowTitle('FSC')
		self.resize(600, 600)
		self.move(300, 300)
		self.create_main_tab()
		self.show()

		sys.exit(app.exec_())


	def create_main_tab(self):
		fscTab(self)




class tabDropDown(QtGui.QWidget):
	def __init__(self):
		super().__init__()
		#add box for this hbox
		self.publisher_menu = QtGui.QComboBox(self)
		self.subscriber_menu = QtGui.QComboBox(self)
		self.layout = QtGui.QHBoxLayout(self)
		self.setLayout(self.layout)
		self.populate_menus()

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
			print(items[x])
			if os.name == 'nt':
				b = items[x].split('\\')[1].split('.')[0]
			else:
				b = items[x].split('/')[1].split('.')[0]
			menu.addItem(b)


class fscEntry(QtGui.QWidget):
	def __init__(self, data_object):
		super().__init__()
		self.data_layout = QtGui.QHBoxLayout()
		self.data = data_object
		self.input_box = QtGui.QTextEdit()
		self.data_layout.addWidget(self.input_box)
		self.output_box = QtGui.QWidget()
		self.output_layout = QtGui.QVBoxLayout(self.output_box)
		self.populate_output()
		self.output_box.setLayout(self.output_layout)
		self.data_layout.addWidget(self.output_box)
		self.setLayout(self.data_layout)


	def populate_output(self):
		dict_ = js.loads(self.data)
		for key in dict_.keys():
			entry = QtGui.QWidget(self.output_box)
			entry_layout = QtGui.QHBoxLayout(entry)
			entry_layout.addWidget(QtGui.QLabel(self.output_box).setText(key))
			temp = QtGui.QTextEdit(self.output_box).setLineWrapMode(QtGui.QTextEdit.NoWrap)
			temp.setReadOnly(True)
			temp.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
			entry_layout.addWidget(temp.insertHtml(dict_[key]))
			self.output_layout.addWidget(entry)


class fscTab(QtGui.QWidget):

	def __init__(self, window, search_term=None, message_type=None, sub_choices=[], pub_choices=[]):
		super().__init__()

		self.parent_window = window

		#Will be used when there is the added capacity to open existing files
		main_tab_layout = QtGui.QVBoxLayout()
		self.setLayout(main_tab_layout)

		drop_down = tabDropDown()

		print('creating tab')


		self.create_new = QtGui.QWidget(self)
		main_tab_layout.addWidget(self.create_new)
		self.create_new_layout =  QtGui.QVBoxLayout()
		self.create_new_layout.addWidget(drop_down)
		self.create_new.setLayout(self.create_new_layout)


		self.selected_options = QtGui.QWidget(self.create_new)
		self.create_new_layout.addWidget(self.selected_options)
		self.selected_options_layout = QtGui.QHBoxLayout()
		self.selected_options.setLayout(self.selected_options_layout)

		self.publisher_choices_UI = QtGui.QWidget(self.selected_options)
		self.publisher_choices_UI_layout = QtGui.QVBoxLayout()
		self.publisher_choices_UI.setLayout(self.publisher_choices_UI_layout)



		self.subscriber_choices_UI = QtGui.QWidget(self.selected_options)
		self.subscriber_choices_UI_layout = QtGui.QVBoxLayout()
		self.subscriber_choices_UI.setLayout(self.subscriber_choices_UI_layout)
		#move the selected options segment to dropdown
		self.selected_options_layout.addWidget(self.subscriber_choices_UI)
		self.selected_options_layout.addWidget(self.publisher_choices_UI)

		self.subscriber_choices = sub_choices
		self.publisher_choices = pub_choices

		self.selected_options_layout.addWidget(self.subscriber_choices_UI)
		self.selected_options_layout.addWidget(self.publisher_choices_UI)

		drop_down.publisher_menu.activated[str].connect(self.run_publisher)
		drop_down.subscriber_menu.activated[str].connect(self.run_subscriber)

		if(search_term == None):
			self.text_entry = QtGui.QLineEdit(self.create_new)
			self.create_new_layout.addWidget(self.text_entry)
			self.create_button = QtGui.QPushButton("Create", self.create_new)
			self.create_button.clicked.connect(self.create_and_refresh)
			self.create_new_layout.addWidget(self.create_button)

		self.search_term = search_term
		self.message_type = message_type
		self.parent_window.addTab(self, "Create Tab")


	def run_publisher(self, text):
		self.publisher_choices.append(text)
		temp = QtGui.QLabel()
		temp.setText(text)
		self.publisher_choices_UI_layout.addWidget(temp)
		self.create_new_publisher(text)

	def run_subscriber(self, text):
		self.subscriber_choices.append(text)
		temp = QtGui.QLabel()
		temp.setText(text)
		self.subscriber_choices_UI_layout.addWidget(temp)
		self.create_new_subscriber(text)

	def create_new_publisher(self, text):
		if(not((self.search_term == None) or (self.message_type == None))):
			pub = getattr(publishers, text)
			pub = getattr(pub, text)
			pub(self.message_type, self.search_term)

	def create_new_subscriber(self, text):
		if(not((self.search_term == None) or (self.message_type == None))):
			sub = getattr(subscribers, text)
			sub = getattr(sub, text)
			new_tab = fscTab(self.parent_window, self.search_term, self.message_type, self.subscriber_choices,self.publisher_choices)
			self.parent_window.addTab(new_tab, self.search_term+" "+text)
			sub(self.message_type, self.search_term, new_tab)



	def create_and_refresh(self):
		self.search_term = self.text_entry.text() #test that this returns None
		self.message_type = 'standard'
		if(((self.search_term is not None) or (self.search_term is not '')) and (self.message_type is not None)):
			for a in reversed(range(self.publisher_choices_UI_layout.count())):
				w = self.publisher_choices_UI_layout.takeAt(a)
				if w is not None:
					w = w.widget()
					w.deleteLater()
			for sub in self.subscriber_choices:
				self.create_new_subscriber(sub)
			for pubs in self.publisher_choices:
				self.create_new_publisher(pubs)



def main():
	fscraper = QtGui.QApplication(sys.argv)

	primary_window = fscWindow()
	fscraper.setActiveWindow(primary_window)
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
			self.parent_window.create_new_layout.addWidget(self.window)


		pub.subscribe(self.listener, self.topic_name)

		print("passed subscriber initialisation")

	def update_frame(self):

		if(self.window):
			self.update_file(self.file_name, self.current_data)
			self.tab_layout.setSpacing(3)
			self.window.setLayout(self.tab_layout)
			self.scroll.setWidget(self.parent_window)
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
			msg_array = self.create_output(msg_array)
		with open('data/'+file, 'w', encoding='utf-8') as f:
			js.dump(msg_array, f)

	def name_file(self, primary_name):
		return str(primary_name) + "_" + str(datetime.datetime.now()).replace("-", "_").replace(" ", "_").replace(":","_").split(".")[0] + ".json"

	def listener(self, arg1):
		print("I've been run")
		self.twitter_call_limit.append(arg1[0])
		arg1 = arg1[1:]
		for x in range(len(arg1)):
			arg1[x] = arg1[x].get_dict()
		self.raw_data += arg1
		self.current_data += arg1
		self.update_file(self.raw_file_name, self.raw_data)
		self.update_frame()


# def funfun(arg1):
	# print('thank fucking god' + arg1)
# pub.subscribe(funfun, 'please')
# pub.sendMessage('please', arg1="findme")
# while(True):
	# pub.sendMessage('please', arg1="find me")

app	= QtGui.QApplication(sys.argv)

fscWindow(app)
