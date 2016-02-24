#!/usr/bin/python
from publishers.TwitterPublisher import TwitterPublisher
from subscribers.TwitterSubscriber import TwitterSubscriber

sub = TwitterSubscriber('standard', 'Trump')
pub = TwitterPublisher('standard', 'Trump')