#!/usr/bin/python
import os
from setuptools import setup, find_packages
setup(
    name = 'fscrape',
    packages = ['fscrape'],
	author = 'Peter Travers',
	author_email = 'peter.travers@abdn.ac.uk',
	license = 'GPLv3',
	version = '0.0.1',
	url='https://github.com/ptravers/fsc',
	install_requires = [
		'application_only_auth',
		'pubsub'
	]
)