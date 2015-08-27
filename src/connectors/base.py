#!/usr/bin/env python
# -*- coding: utf-8 -*-

# system modules
import os.path

class Connector(object):
	def __init__(self):
		self._fileroles = []
		self._at_least = dict()
		self._at_most = dict()
		self._type = None
		self._filenames = dict()
		self._directory = None

	def add_filerole(self, label, at_least=None, at_most=None):
		self._fileroles.append(label)
		if at_least is not None:
			self._at_least[label] = at_least
		if at_most is not None:
			self._at_most[label] = at_most
		self._filenames[label] = []

	def _parse_rolefile(self, rolefile):
		if self._type is None:
			raise NotImplementedError()

		fileroles = rolefile.items(self._type)
		for filerole, filenames in fileroles:
			if filerole not in self._fileroles:
				raise ValueError(('E0012:Invalid file role %s.' % filerole))
			filenames = filenames.split('\n')
			filenames = map(str.strip, filenames)
			self._filenames[filerole] += filenames

		for filerole in self._fileroles:
			if filerole in self._at_least:
				if len(self._filenames[filerole]) < self._at_least[filerole]:
					raise ValueError('E0010:Too few entries for %s' % filerole)
			if filerole in self._at_most:
				if len(self._filenames[filerole]) > self._at_most[filerole]:
					raise ValueError('E0011:Too many entries for %s' % filerole)

	def _read_textfile_in_memory(self, filename):
		try:
			if self._directory is not None:
				filename = os.path.join(self._directory, filename)
			lines = open(filename, 'r').readlines()
		except IOError:
			raise TypeError('E0013:Unable to open file %s' % filename)
		except:
			raise TypeError('E0012:Unable to read file %s' % filename)

		return lines