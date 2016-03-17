#!/usr/bin/python
from PyQt4 import QtGui, QtCore
import sys
import os



class fscEntry(QtGui.QWidget):
	def __init__(self, data_object, parent=None):
		super(fscEntry, self).__init__(parent)
		self.data = data_object
		
		self.data_layout = QtGui.QVBoxLayout(self)
		self.input_box = None
		self.output_items = []
		self.populate_output(self.data)

	def get_input_data(self):
		output = self.input_box.text()
		return output
	
	def populate_output(self, data_dict):
		if isinstance(data_dict, dict):
			for key in data_dict.keys():
			#checks if the element being added is a list or a string/int to avoid type problems
				entry = QtGui.QWidget(self)
				entry_layout = QtGui.QHBoxLayout()
				entry.setLayout(entry_layout)
				entry_label = QtGui.QLabel(self)
				entry_label.setText(key)
				entry_layout.addWidget(entry_label)
				if isinstance(data_dict[key], list):
						text = ""
						widget = QtGui.QLabel(self)
						if key == 'mentions':
							for x in data_dict[key]:
								text += x['screen_name'] + " : " + x['id_str'] + ", "
						elif key == 'hashtags':
							for x in data_dict[key]:
								text += x['text'] + ", "
						widget.setText(text)
						entry_layout.addWidget(widget)
						self.data_layout.addWidget(entry)
						self.output_items.append([widget, entry])
						
				else:
					if(key == 'node' or key == 'comment'):
						temp = QtGui.QLineEdit(self)
						#temp.setLineWrapMode(QtGui.QTextEdit.NoWrap)
						#temp.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
						temp.setReadOnly(False) if (key == 'node') else temp.setReadOnly(True)
						if (key == 'node'):
							self.input_box = temp
						temp.setText(data_dict[key])
					else :
						temp = QtGui.QLabel(self)
						temp.setText(data_dict[key])
					entry_layout.addWidget(temp)
					self.data_layout.addWidget(entry)
					self.output_items.append([temp, entry])
