#!/usr/bin/python
import json as js
from messages.StandardMessage import StandardMessage
from pubsub import pub

class FacebookPublisher():

	def __init__(self):
		#initliasie the publisher
		self.name = 'Facebook'
		
	def publish(self):
		return 'This exists'
		#this is where the publishing segment should go