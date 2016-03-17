#!/usr/bin/python
import json as js
from pubsub import pub
from publishers.TwitterClient import Client
from messages.StandardMessage import StandardMessage

API_KEY, API_SECRET = ('5jquzflYqTUNMNqmpdxPUr4Si', 'RE3tNfpjyhNB5IJatzLiDnoonEw7i2OgWz0o5kSCbS2egllDBv')


class TwitterPublisher:
	def __init__(self, message, term, count = 5):
		self.client = Client(API_KEY, API_SECRET)
		self.message_type = message
		self.search_term = term
		self.count = count
		self.search_link_base = 'https://api.twitter.com/1.1/search/tweets.json?q='
		self.link_base = 'https://twitter.com/'
		self.puiblish()

	#Get rate limit when the rate limit is less than the count given the system
	#must request rate_limit. Then enter waiting state

	def get_data(self, count):
		search_link = self.search_link_base + self.search_term + "&count=" + str(count)
		output = self.client.request(search_link)
		msg_array = []
		msg_array.append(self.get_rate())
		for x in range(len(output.get('statuses'))):
			msg = StandardMessage()
			msg.mentions = output.get('statuses')[x]['entities']['user_mentions']
			msg.id = output.get('statuses')[x]['id_str']
			msg.shares = str(output.get('statuses')[x]['retweet_count'])
			msg.likes = str(output.get('statuses')[x]['favorite_count'])
			msg.hashtags = output.get('statuses')[x]['entities']['hashtags']
			msg.url = self.link_base + output.get('statuses')[x]['user']['screen_name'] + '/status/' + msg.id
			msg.comment = str(output.get('statuses')[x]['text'])
			msg.followers = str(output.get('statuses')[x]['user']['followers_count'])
			msg.following = str(output.get('statuses')[x]['user']['friends_count'])
			msg.shared = str(output.get('statuses')[x]['retweeted'])
			msg_array.append(msg)
		return msg_array
	
	
	def get_rate(self):
		i = self.client.rate_limit_status()['resources']['search']
		return i

	def puiblish(self):
		msg = self.get_data(self.count)
		pub.sendMessage(self.search_term, arg1=msg)

