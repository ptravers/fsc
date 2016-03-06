#!/usr/bin/python
import publishers
import subscribers
import messages
from PyQt4 import QtGui, QtCore
import sys
import os



class fscWindow(QtGui.QTabWidget):

	def __init__(self, parent):
		super().__init__()
		parent.setActiveWindow(self)
		
		pubs_n_subs = []
		
		self.setWindowTitle('FSC')
		self.resize(600, 600)
		self.move(300, 300)
		self.create_main_tab()
		self.show()

		sys.exit(app.exec_())


	def create_main_tab(self):
		fscTab(self)