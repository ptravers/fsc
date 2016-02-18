#!/usr/bin/python
import json as js

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
		
	def get_message(self):
		output = js.dumps(self.__dict__)
		return output