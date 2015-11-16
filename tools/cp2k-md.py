#!/usr/bin/env python

import argparse
import requests as r

baseurl = 'http://localhost:8000/results/api/'
system = 'hematite-IOH3'
bucket = 'TOKEN'
bucket_name = 'test'
series = 'production'
basepath = '/Volumes/ALFA/bumblebee-test/IOHMD-A-prod-22ce9a183b38cedfca608118c1fc99f9/run-0/'

parser = argparse.ArgumentParser()
parser.add_argument('bucket', help='Bucket to save the data to.')


class BumblebeeApi(object):
	def __init__(self, baseurl):
		try:
			self._urls = r.get(baseurl).json()
		except:
			raise ValueError('Unable to connect to server.')

	def get_if_exists(self, objecttype, multiple=False, **kwargs):
		if objecttype not in self._urls:
			raise ValueError('Object type not known on server side.')

		result = r.get(self._urls[objecttype], params=kwargs).json()
		if not multiple and len(result) > 1:
			raise ValueError('Filter criteria not narrow enough: non-unique answer from server.')
		if len(result) == 0:
			return None
		if multiple:
			return result
		else:
			return result[0]

	def create_if_missing(self, objecttype, **kwargs):
		instance = self.get_if_exists(objecttype, **kwargs)
		if instance is None:
			instance = self.create(objecttype, **kwargs)
		return instance

	def create(self, objecttype, **kwargs):
		if objecttype not in self._urls:
			raise ValueError('Object type not known on server side.')

		result = r.post(self._urls[objecttype], data=kwargs)
		if result.status_code != 201:
			raise ValueError('Unable to add new entry because of the following server answer: ' + str(result.json()))
		return result.json()


class CP2KParser(object):
	def __init__(self, logfile=None, inputfile=None, restartfile=None, coordfile=False):
		self._logfile = open(logfile).readlines()
		self._inputfile = [_.strip() for _ in open(inputfile).readlines()]
		self._restartfile = open(restartfile).readlines()
		self._coordfile = coordfile

	def get_mdrun_desired(self, kind):
		path = dict((
			('timestep', 'MOTION / MD / TIMESTEP'),
			('temperature', 'MOTION / MD / TEMPERATURE'),
			('pressure', 'MOTION / MD / BAROSTAT / PRESSURE'),
			('multiplicity', 'FORCE_EVAL / DFT / MULTIPLICITY')
		))[kind]
		if self._inputfile is not None:
			return self.get_path(path)

	def get_path(self, path):
		elements = path.split(' / ')
		sections = []
		line_numbers = []
		collect = []
		for no, line in enumerate(self._inputfile):
			if len(line) == 0 or line.startswith('#') or line.startswith('!'):
				continue
			if line.startswith('&END'):
				ending = line[4:].strip()
				if ending != '' and ending != sections[-1]:
					raise ValueError('Trying to end the %s section from line %d with %s in line %d' % (
					sections[-1], line_numbers[-1] + 1, ending, no + 1))
				sections = sections[:-1]
				line_numbers = line_numbers[:-1]
				continue

			if line.startswith('&'):
				sections.append(line.split()[0][1:])
				line_numbers.append(no)
				continue

			if sections == elements[:-1]:
				if elements[-1] == '*':
					collect.append(line)
					continue
				parts = line.split()
				if parts[0] == elements[-1]:
					return ' '.join(parts[1:])
		if elements[-1] == '*':
			return collect
		return None

bb = BumblebeeApi(baseurl)

# get meta data
server_system = bb.create_if_missing('system', name=system)
server_bucket = bb.create_if_missing('bucket', token=bucket, name=bucket_name, system=server_system['id'])
server_series = bb.create_if_missing('series', bucket=server_bucket['id'], name=series)

# get MD run
highest_part = bb.get_if_exists('mdrun', series=server_series['id'], multiple=True)
if highest_part is None:
	highest_part = 1
else:
	highest_part = max([_['part'] for _ in highest_part]) + 1
server_mdrun = bb.create('mdrun', series=server_series['id'], part=highest_part)

# notify user
print 'Loading data into %s.%s.%s.%d' % (server_system['name'], server_bucket['token'], server_series['name'], server_mdrun['part'])

# load CP2K data
cp = CP2KParser(basepath + 'run.log', basepath + 'run.inp', basepath + 'run.base', basepath + '/traj/pos-pos-1.dcd')
settings = dict()
for setting in 'temperature pressure multiplicity timestep'.split():
	try:
		settings[setting] = float(cp.get_mdrun_desired(setting))
	except:
		settings[setting] = None
server_settings = bb.create('mdrunsettings', mdrun=server_mdrun['id'], **settings)
