#!/usr/bin/env python
# coding: utf8
from gluon import *

class Error:
	def __init__(self, code=None):
		self.code = code
		self.reason = None
		self.info = None


	def set_error(self, code=None, message=None, info=None):
		# Set error details based on error code
		if not code:
			code = self.code
		else:
			self.code = code

		if code == 'Input01':
			self.reason = 'Missing expected input value'
		elif code == 'Input02':
			self.reason = 'Invalid input provided'
		elif code == 'Input03':
			self.reason = 'Invalid or non-existent identifier'
		elif code == 'Input04':
			self.reason = 'Invalid input length'
		elif code == 'Media01':
			self.reason = 'Unknown media type'
		elif code == 'Media02':
			self.reason = 'Media does not exist'
        elif code == 'Acc01':
            self.reason = 'Account does not exist'
		else:
			self.code = 'Unknown01'
			self.reason = 'Unknown error'

		self.info = info

		if message:
			self.reason += ': ' + message

		return True