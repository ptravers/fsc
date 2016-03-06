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
		self.followers = "null"
		self.following = "null"

	def get_dict(self):
		return self.__dict__

	def get_message(self):
		return js.dumps(self.__dict__, sort_keys=True, indent=4, separators=(',', ':'))

	def get_comment(self):
		return self.comment