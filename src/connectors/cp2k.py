#!/usr/bin/env python
# -*- coding: utf-8 -*-

# system modules
import re

# package modules
import base

def _find_by_re(lines, pattern, maxcount = None):
	found = []
	for line in lines:
		res = re.findall(pattern, line)
		if res != []:
			found.append(res[0])
		if maxcount is not None and len(found) >= maxcount:
			break
	if maxcount == 1:
		if len(found) > 0:
			return found[0]
		else:
			return None
	return found

class Cp2kConnector(base.Connector):
	def __init__(self, rolefile, directory=None):
		super(Cp2kConnector, self).__init__()
		self._directory = directory
		self._type = 'cp2k'
		self.add_filerole('logfile', at_least=1, at_most=1)
		self._parse_rolefile(rolefile)

	def parse(self, db, bucket_id, run_id):
		loglines = self._read_textfile_in_memory(self._filenames['logfile'][0])

		db_run = db.runs.find_one({'_id': run_id})
		try:
			db_run['cores'] = int(_find_by_re(loglines, '^GLOBAL| Total number of message passing processes[ ]*(\d*)', 1))
		except:
			pass
		try:
			db_run['ensemble'] = _find_by_re(loglines, '^MD| Ensemble Type [ ]* ([^ ]*)', 1)
		except:
			pass
		try:
			db_run['ts'] = float(_find_by_re(loglines, '^MD| Time Step \[fs\] [ ]* (\d*\.\d*)', 1))
		except:
			pass
		db.runs.update({'_id': run_id}, {'$set': db_run}, upsert=False)