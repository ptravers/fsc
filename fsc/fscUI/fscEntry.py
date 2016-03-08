#!/usr/bin/python
from PyQt4 import QtGui, QtCore
import sys
import os



class fscEntry(QtGui.QWidget):
	def __init__(self, data_object):
		super().__init__()
		self.data_layout = QtGui.QHBoxLayout(self)
		self.data = data_object
		self.input_box = QtGui.QTextEdit(self)
		self.input_box.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
		self.data_layout.addWidget(self.input_box)
		self.output_box = QtGui.QWidget(self)
		self.output_layout = QtGui.QVBoxLayout()
		
		self.output_box.setLayout(self.output_layout)
		self.data_layout.addWidget(self.output_box)
		self.setLayout(self.data_layout)
		self.output_items = []
		self.populate_output(self.data)

	def get_input_data(self):
		self.input_box.toPlainText()
	
	def populate_output(self, data_dict):
		if isinstance(data_dict, dict):
			for key in data_dict.keys():
				
				if isinstance(data_dict[key], list):
					pass
				else:
					entry = QtGui.QWidget(self.output_box)
					entry_layout = QtGui.QHBoxLayout()
					entry.setLayout(entry_layout)
					entry_label = QtGui.QLabel(self.output_box)
					entry_label.setText(key)
					entry_layout.addWidget(entry_label)
					temp = QtGui.QLabel(self.output_box)
					#temp.setLineWrapMode(QtGui.QTextEdit.NoWrap)
					#temp.setReadOnly(True)
					#temp.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
					temp.setText(data_dict[key])
					entry_layout.addWidget(temp)
					self.output_layout.addWidget(entry)
					self.output_items.append([temp, entry])
