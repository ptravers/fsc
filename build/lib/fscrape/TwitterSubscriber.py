#!/usr/bin/python
from pubsub import pub
import json as js

class TwitterSubscriber:
	def __init__(self, msg_type, term):
		self.term = term
		self.msg_type = msg_type
		pub.subscribe(self.listener, self.term)

	def listener(self, arg1):
		print(arg1)