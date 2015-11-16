#!/usr/bin/env python

import argparse
import requests as r

baseurl = 'http://localhost:8000/results/api/'
system = 'hematite-IOH3'
bucket = 'TOKEN'
bucket_name = 'test'
series = 'production'

parser = argparse.ArgumentParser()
parser.add_argument('bucket', help='Bucket to save the data to.')


class BumblebeeApi(object):
	def __init__(self, baseurl):
		try:
			self._urls = r.get(baseurl).json()
		except:
			raise ValueError('Unable to connect to server.')

	def get_if_exists(self, objecttype, **kwargs):
		if objecttype not in self._urls:
			raise ValueError('Object type not known on server side.')

		result = r.get(self._urls[objecttype], params=kwargs).json()
		if len(result) > 1:
			raise ValueError('Filter criteria not narrow enough: non-unique answer from server.')
		if len(result) == 1:
			return result[0]
		else:
			return None

	def create(self, objecttype, **kwargs):
		if objecttype not in self._urls:
			raise ValueError('Object type not known on server side.')

		result = r.post(self._urls[objecttype], data=kwargs)
		if result.status_code != 201:
			raise ValueError('Unable to add new entry because of the following server answer: ' + str(result.json()))
		return result.json()


class CP2KParser(object):
	def __init__(self, logfile=None, inputfile=None, coordfile=False):
		self._logfile = logfile
		self._inputfile = inputfile
		self._coordfile = coordfile

	def get_mdrun_desired(self, kind):
		path = dict((
			('temperature', 'foobar'),
			('pressure', 'snafu'),
		))[kind]
		if self._inputfile is not None:
			return self._get_config_path(path)


bb = BumblebeeApi(baseurl)

# get system
server_system = bb.get_if_exists('system', name=system)
if server_system is None:
	print 'Creating new system.'
	server_system = bb.create('system', name=system)

# get bucket
server_bucket = bb.get_if_exists('bucket', token=bucket, name=bucket_name, system=server_system['id'])
if server_bucket is None:
	print 'Creating new bucket.'
	server_bucket = bb.create('bucket', token=bucket, name=bucket_name, system=server_system['id'])

print server_bucket

# get series
server_series = bb.get_if_exists('series', bucket=server_bucket['id'], name=series)
if server_series is None:
	print 'Creating new series.'
	server_series = bb.create('series', bucket=server_bucket['id'], name=series)

print server_series