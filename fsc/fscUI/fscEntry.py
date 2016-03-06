#!/usr/bin/python
from PyQt4 import QtGui, QtCore
import sys
import os



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
