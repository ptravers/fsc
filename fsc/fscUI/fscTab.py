#!/usr/bin/python
import publishers
import subscribers
import messages
from PyQt4 import QtGui, QtCore
import sys
import os
from .tabDropDown import tabDropDown



class fscTab(QtGui.QWidget):

	def __init__(self, window, search_term=None, message_type=None, sub_choices=[], pub_choices=[]):
		super().__init__()

		self.parent_window = window

		#Will be used when there is the added capacity to open existing files
		main_tab_layout = QtGui.QVBoxLayout()
		self.setLayout(main_tab_layout)

		drop_down = tabDropDown()


		self.create_new = QtGui.QWidget(self)
		main_tab_layout.addWidget(self.create_new)
		self.create_new_layout =  QtGui.QVBoxLayout()
		self.create_new_layout.addWidget(drop_down)
		drop 
		self.create_new.setLayout(self.create_new_layout)


		# self.selected_options = QtGui.QWidget(self.create_new)
		# self.create_new_layout.addWidget(self.selected_options)
		# self.selected_options_layout = QtGui.QHBoxLayout()
		# self.selected_options.setLayout(self.selected_options_layout)

		# self.publisher_choices_UI = QtGui.QWidget(self.selected_options)
		# self.publisher_choices_UI_layout = QtGui.QVBoxLayout()
		# self.publisher_choices_UI.setLayout(self.publisher_choices_UI_layout)



		# self.subscriber_choices_UI = QtGui.QWidget(self.selected_options)
		# self.subscriber_choices_UI_layout = QtGui.QVBoxLayout()
		# self.subscriber_choices_UI.setLayout(self.subscriber_choices_UI_layout)
		# #move the selected options segment to dropdown
		# self.selected_options_layout.addWidget(self.subscriber_choices_UI)
		# self.selected_options_layout.addWidget(self.publisher_choices_UI)

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
			self.parent_window.addTab(self, "Create Tab")

		self.search_term = search_term
		self.message_type = message_type


	def run_publisher(self, text):
		self.publisher_choices.append(text)
		temp = QtGui.QLabel()
		temp.setText(text)
		self.create_new_layout.addWidget(temp)
		self.create_new_publisher(text)

	def run_subscriber(self, text):
		self.subscriber_choices.append(text)
		temp = QtGui.QLabel()
		temp.setText(text)
		self.create_new_layout.addWidget(temp)
		self.create_new_subscriber(text)

	def create_new_publisher(self, text):
		if(not((self.search_term == None) or (self.message_type == None))):
			pub = getattr(publishers, text)
			pub = getattr(pub, text)
			temp_pub = pub(self.message_type, self.search_term)
			self.parent_window.pubs_n_subs.append(temp_pub)

	def create_new_subscriber(self, text):
		if(not((self.search_term == None) or (self.message_type == None))):
			sub = getattr(subscribers, text)
			sub = getattr(sub, text)
			new_tab = fscTab(self.parent_window, self.search_term, self.message_type, self.subscriber_choices,self.publisher_choices)
			self.parent_window.addTab(new_tab, self.search_term+" "+text)
			temp_sub = sub(self.message_type, self.search_term, new_tab)
			self.parent_window.pubs_n_subs.append(temp_sub)



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