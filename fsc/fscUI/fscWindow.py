#!/usr/bin/python
import publishers
import subscribers
import messages
from .fscTab import fscTab
from PyQt4 import QtGui, QtCore
import sys
import os



class fscWindow(QtGui.QTabWidget):

	def __init__(self, parent):
		super().__init__()
		parent.setActiveWindow(self)
		
		self.pubs = []
		self.subs = []
		
		self.setWindowTitle('FSC')
		self.resize(600, 600)
		self.move(300, 300)
		self.create_main_tab()
		self.show()

		sys.exit(parent.exec_())


	def create_main_tab(self):
		fscTab(self)
		
	def run(self):
		self.run_publishers()
		
	def run_publishers(self):
		for pub in pubs:
			pub.publish()
	
	def run_subscribers(self):
		for sub in subs:
			sub.update_frame()