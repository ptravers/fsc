#!/usr/bin/python
from pubsub import pub
import json as js
from application_only_auth import Client

API_KEY, API_SECRET = ('5jquzflYqTUNMNqmpdxPUr4Si', 'RE3tNfpjyhNB5IJatzLiDnoonEw7i2OgWz0o5kSCbS2egllDBv')

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
		
	def get_message(self):
		return js.dumps(self.__dict__, sort_keys=True, indent=4, separators=(',', ':'))



class TwitterPublisher:
	def __init__(self, message, term):
		self.client = Client(API_KEY, API_SECRET)
		self.message_type = message
		self.search_term = term
		self.search_link_base = 'https://api.twitter.com/1.1/search/tweets.json?q='
		self.link_base = 'https://twitter.com/'
		self.run()
	
	#Get rate limit when the rate limit is less than the count given the system
	#must request rate_limit. Then enter waiting state
	
	def get_data(self, count):
		search_link = self.search_link_base + self.search_term + "&count=" + str(count)
		print(search_link)
		output = self.client.request(search_link)
		msg_array = []
		msg_array.append(self.get_rate())
		for x in range(len(output.get('statuses'))):
			print(x)
			msg = StandardMessage()
			msg.mentions = output.get('statuses')[x]['entities']['user_mentions']
			msg.shares = str(output.get('statuses')[x]['retweet_count'])
			msg.likes = str(output.get('statuses')[x]['favorite_count'])
			msg.hashtags = output.get('statuses')[x]['entities']['hashtags']
			msg.url = self.link_base + output.get('statuses')[x]['user']['screen_name'] + '/' + output.get('statuses')[0]['id_str']
			msg.comment = str(output.get('statuses')[x]['text'])
			msg.shared = str(output.get('statuses')[x]['retweeted'])
			msg_array.append(msg)
		return msg_array
	
	def get_rate(self):
		i = self.client.rate_limit_status()['resources']['search']
		return i
	
	#This should be placed in the Parent class should be passed a message a string and the publisher object
	def run(self):
		msg = self.get_data(400)
		pub.sendMessage(self.search_term, arg1=msg)
		

class TwitterSubscriber:
	def __init__(self, msg_type, term):
		self.term = term
		self.msg_type = msg_type
		pub.subscribe(self.listener, self.term)

	def listener(self, arg1):
		print(arg1[0])
		
		
sub = TwitterSubscriber('standard', 'Trump')
pub = TwitterPublisher('standard', 'Trump')
