#!/usr/bin/env python

import sys
import requests as r

baseurl = 'http://localhost:8000/results/api/'
system = 'test'


class BumblebeeApi(object):
	def __init__(self, baseurl):
		self._urls = r.get(baseurl).json()

	def exists(self, objecttype, **kwargs):
		if objecttype not in self._urls:
			raise ValueError('Object type not known on server side.')

		result = r.get(self._urls[objecttype], params=kwargs).json()
		if len(result) > 1:
			raise ValueError('Filter criteria not narrow enough: non-unique answer from server.')
		return len(result) == 0

bb = BumblebeeApi(baseurl)
bb.exists('series', name=system)