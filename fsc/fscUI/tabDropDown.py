#!/usr/bin/python
import publishers
import subscribers
import messages
from PyQt4 import QtGui, QtCore
import sys
import os



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
